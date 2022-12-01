import db
import imaging
import pathlib

from ury_wrapped.tasks import TASKS


def generate(memberid: int):
    pathlib.Path("./results/" + str(memberid)).mkdir(parents=True, exist_ok=True)
    for name, query, formatter in TASKS:
        result = db.query_one(query, memberid)
        if result is None:
            raise Exception("query for task %s returned no results" % name)
        imaging.make_image(formatter(result), f"results/{memberid}/{name}.png")


if __name__ == "__main__":
    memberid = int(input("Enter member ID:\n> "))
    generate(memberid)
