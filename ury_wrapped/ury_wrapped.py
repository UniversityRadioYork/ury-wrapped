import db
import imaging
import pathlib

TASKS = [
    (
        "top_song",
        """
  with timeslots as (
    select show_season_timeslot_id
    from sis2.member_signin
    where memberid = %s
      and sign_time >= '2022-01-01'
),
     tracks as (
         select coalesce(rt.title, tn.track) || ' - ' || coalesce(rt.artist, tn.artist) as title
         from tracklist.tracklist
                  inner join timeslots on tracklist.timeslotid = timeslots.show_season_timeslot_id
                  left join tracklist.track_notrec tn on tracklist.audiologid = tn.audiologid
                  left join tracklist.track_rec tr on tracklist.audiologid = tr.audiologid
                  left join rec_track rt on tr.trackid = rt.trackid
     )
select title, count(title) as cnt
from tracks
group by title
order by cnt desc
  """,
        lambda result: f"Your most played song this year was {result[0]}, which you played {result[1]} times.",
    ),
    (
        "time_on_air",
        """
      with timeslots as (
    select ts.*
    from sis2.member_signin si
             inner join schedule.show_season_timeslot ts using (show_season_timeslot_id)
    where si.memberid = %s
      and si.sign_time >= '2022-01-01'
)
select count(timeslots), sum(timeslots.duration) as duration
from timeslots
""",
        lambda result: f"You presented {result[0]} shows this year, spending {result[1].days*24 + result[1].seconds//3600} hours on air.",
    ),
]


def generate(memberid: int):
    pathlib.Path("./results/" + str(memberid)).mkdir(parents=True, exist_ok=True)
    for name, query, formatter in TASKS:
        result = db.query_one(query, memberid)
        imaging.make_image(formatter(result), f"results/{memberid}/{name}.png")


if __name__ == "__main__":
    memberid = int(input("Enter member ID:\n> "))
    generate(memberid)
