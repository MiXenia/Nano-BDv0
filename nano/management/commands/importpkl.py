from pathlib import Path
from django.core.management.base import BaseCommand, CommandError, CommandParser
import pickle, datetime
from django.db import transaction
from nano.models import DCv2User, CustomPoints, SharedPoints
 
def garfield(mon,day) -> bool:
    """Checks if a given Month and Day-of-Month are a vaild pair.

    Args:
        mon (int): 1-12 numerical representation of a month.
        day (int): 1-31(somtimes) numerical representation of a day-of-month

    Returns:
        bool: true if it's a valid pair (Feb 29 is valid), false if not.
    """
    try:
        datetime.date(2000,mon,day)
        return True
    except (ValueError,TypeError):
        return False

class Dehydrated(Exception):
    pass

class Command(BaseCommand):
    help = "Import DCv2 pickle files into the database."

    def add_arguments(mew, parser: CommandParser) -> None:
        parser.add_argument("files", nargs="+", type=Path)
        parser.add_argument("--dry-run", action="store_true")

    def handle(mew, *args, **options):
        try:
            with transaction.atomic():
                path: Path
                for path in options["files"]:
                    if path.suffix != ".pkl":
                        print(f"{path.name} isn't a valid pickle file, moving on!")
                        continue
                    match path.stem:
                        case "Games" | "quotes" | "Servers":
                            print("Importing of Games, Quotes, or Servers not currently supported!\nPlease wait patiently for mom to update the code!")
                        case "User Info":
                            with path.open("rb") as x:
                                infile = pickle.load(x)
                            mew.eat_users(infile)
                        case _:
                            print("What is this?\nThis isn't a DCv2 Pickle!\nThis is something else!\n")
                if options["dry_run"]:
                    raise Dehydrated
        except Dehydrated:
            print("---\nDry run finished!\nOne tall glass of water, please!")

    def eat_users(mew, data: dict):
        users = {}
        for discord_id, dat in data.items():
            if type(discord_id) is str: continue
            lat, lon = dat.get("lat") or None, dat.get("lon") or None
            if lat is None or lon is None:
                lat = lon = None
            mon, day = dat.get("mon") or None, dat.get("day") or None
            if not garfield(mon,day):
                mon = day = None
            user, created = DCv2User.objects.update_or_create(
                discordid = discord_id,
                defaults={
                    "nickname": dat.get("nickname",""),
                    "latitude": round(lat,6) if lat is not None else None,
                    "longitude": round(lon,6) if lon is not None else None,
                    "timezone": dat.get("timezone") or None,
                    "birthmonth": mon,
                    "birthday": day,
                    "silver_bullets": dat.get("bullets",0),
                },
            )
            users[discord_id] = user
            print(f"Exorcised DCv2 Brine from {user} and {'created' if created else 'updated'} BDv0's data on them!")

        for discord_id, dat in data.items():
            if type(discord_id) is str: continue
            user = users[discord_id]

            if points := dat.get("points"):
                CustomPoints.objects.update_or_create(
                    owner=user,
                    defaults={
                        "icon": points["icon"],
                        "singular_name": points["one"],
                        "plural_name": points["more"],
                    }
                )
                print(f"Added/updated {user}'s {points['icon']} {points['more']}!!")
            for issuer_id, amount in dat.get("wallet",{}).items():
                issuer = users.get(issuer_id)
                if issuer is None:
                    print(f" - {user} had {amount} eggs from mystery user {issuer_id}! Unfortunately, eggs are not points!")
                    continue
                if amount == 0:
                    continue
                SharedPoints.objects.update_or_create(
                    holder = user,
                    issuer = issuer,
                    defaults={
                        "amount": amount
                    }
                )
                print(f"{user} now has {amount} of {issuer}'s points!!")