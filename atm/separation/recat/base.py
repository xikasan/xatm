# -*- coding: utf-8 -*-

R = 2.5

distance_based_separation_table = dict(
    index=dict(
        leader=False,
        follower=False,
    ),
    table=dict(
        A=dict(A=3, B=4, C=5, D=5, E=6, F=8),
        B=dict(A=R, B=3, C=4, D=4, E=5, F=7),
        C=dict(A=R, B=R, C=3, D=3, E=4, F=6),
        D=dict(A=R, B=R, C=R, D=R, E=R, F=5),
        E=dict(A=R, B=R, C=R, D=R, E=R, F=4),
        F=dict(A=R, B=R, C=R, D=R, E=R, F=3),
    )
)

time_based_separation_table = dict(
    index=dict(
        leader=False,
        follower=True,
    ),
    table=dict(
        D=dict(
            A=dict(A=77, B=103, C=129, D=129, E=154, F=206),
            B=dict(A=73, B= 88, C=119, D=117, E=146, F=205),
            C=dict(A=75, B= 75, C= 90, D= 90, E=120, F=180),
            D=dict(A=75, B= 75, C= 75, D= 75, E= 75, F=150),
            E=dict(A=82, B= 82, C= 82, D= 82, E= 82, F=131),
            F=dict(A=82, B= 82, C= 82, D= 82, E= 82, F= 98),
        ),
        A=dict(
            A=dict(A=77, B=103, C=129, D=129, E=154, F=206),
            B=dict(A=64, B= 77, C=103, D=103, E=128, F=180),
            C=dict(A=75, B= 75, C= 90, D= 90, E=120, F=180),
            D=dict(A=74, B= 74, C= 74, D= 74, E= 74, F=148),
            E=dict(A=82, B= 82, C= 82, D= 82, E= 82, F=131),
            F=dict(A=82, B= 82, C= 82, D= 82, E= 82, F= 98),
        )
    )
)

# A=dict(A=, B=, C=, D=, E=, F=)
