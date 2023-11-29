from typing import Callable, List, NamedTuple, Tuple


class Task(NamedTuple):
    name: str
    query: str
    formatter: Callable[[Tuple], str]


TASKS: List[Task] = [
    Task(
        "top_song",
        """
        with timeslots as (
          select show_season_timeslot_id
          from sis2.member_signin
          where memberid = %s
            and sign_time >= '2023-01-01'
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
    Task(
        "time_on_air",
        """
        with timeslots as (
          select ts.*
          from sis2.member_signin si
                  inner join schedule.show_season_timeslot ts using (show_season_timeslot_id)
          where si.memberid = %s
            and si.sign_time >= '2023-01-01'
      )
      select count(timeslots), sum(timeslots.duration) as duration
      from timeslots
      """,
        lambda result: f"You presented {result[0]} shows this year, spending {result[1].days*24 + result[1].seconds//3600} hours on air.",
    ),
    Task(
        "top_artist",
        """
            with timeslots as (
            select show_season_timeslot_id
            from sis2.member_signin
            where memberid = %s
              and sign_time >= '2023-01-01'
        ),
            tracks as (
                select coalesce(rt.artist, tn.artist) as artist
                from tracklist.tracklist
                          inner join timeslots on tracklist.timeslotid = timeslots.show_season_timeslot_id
                          left join tracklist.track_notrec tn on tracklist.audiologid = tn.audiologid
                          left join tracklist.track_rec tr on tracklist.audiologid = tr.audiologid
                          left join rec_track rt on tr.trackid = rt.trackid
            )
        select artist, count(artist) as cnt
        from tracks
        group by artist
        order by cnt desc
        """,
        lambda result: f"Your most played artist was {result[0]} - you played their songs a total of {result[1]} times.",
    ),
    Task(
        "listen_time",
        """
        with timeslots as (
          select ts.*
          from sis2.member_signin si
                  inner join schedule.show_season_timeslot ts using (show_season_timeslot_id)
          where si.memberid = %s
            and si.sign_time >= '2023-01-01'
        )
        select sum(l.time_end - l.time_start) as listeners_time_wasted
        from listens.listen l
                inner join timeslots ts
                            on l.time_start between ts.start_time - '10 minutes'::interval and ts.start_time + ts.duration + '10 minutes'::interval and
                              l.time_end between ts.start_time - '10 minutes'::interval and ts.start_time + ts.duration + '10 minutes'::interval
        where l.time_end - l.time_start < '12 hours'::interval
        """,
        lambda total: f"People wasted {total[0].days*24 + total[0].seconds//3600} hours of their lives listening to you this year.",
    ),
    Task(
        "first_song",
        """
      with timeslots as (
        select show_season_timeslot_id
        from sis2.member_signin
        where memberid = %s
          and sign_time >= '2023-01-01'
      )
      select coalesce(rt.title, tn.track) as track, coalesce(rt.artist, tn.artist) as artist
      from tracklist.tracklist
              inner join timeslots on tracklist.timeslotid = timeslots.show_season_timeslot_id
              left join tracklist.track_notrec tn on tracklist.audiologid = tn.audiologid
              left join tracklist.track_rec tr on tracklist.audiologid = tr.audiologid
              left join rec_track rt on tr.trackid = rt.trackid
      limit 1""",
        lambda res: f"The first song you played this year was {res[0]} by {res[1]}.",
    ),
    Task(
        "different_tracks",
        """
      with timeslots as (
        select show_season_timeslot_id
        from sis2.member_signin
        where memberid = %s
          and sign_time >= '2023-01-01'
      ),
        tracks as (
            select coalesce(rt.title, tn.track) || ' - ' || coalesce(rt.artist, tn.artist) as title
            from tracklist.tracklist
                      inner join timeslots on tracklist.timeslotid = timeslots.show_season_timeslot_id
                      left join tracklist.track_notrec tn on tracklist.audiologid = tn.audiologid
                      left join tracklist.track_rec tr on tracklist.audiologid = tr.audiologid
                      left join rec_track rt on tr.trackid = rt.trackid
        )
      select count(distinct title)
      from tracks
      """,
        lambda result: f"You played {result[0]} different songs this year - quite the adventurer.",
    ),
]
