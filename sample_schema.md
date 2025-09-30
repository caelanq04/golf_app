| courses |
| ------------- |
| id (PK) |
| name |
| location |
| api_id |


| holes |
| ------------- |
| id (pk) |
| course_id (fk) |
| hole_number (1-18) |
| par |
| yardage |

| users |
| ------------- |
| id (pk) |
| username |
| email |

| scorecard |
| ------------- |
| id (pk) |
| course_id (fk) |
| user_id (fk) |
| date_played |
| scoring_mode  |

| scores |
| ------------- |
| id (pk) |
| scorecard (fk) |
| hole_id |
| hole_num |
| strokes |
| par_override  |




