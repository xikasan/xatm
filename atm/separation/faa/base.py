# -*- coding: utf-8 -*-

R = 2.5

distance_based_separation = dict(
    index=dict(
        leader=False,
        follower=False,
    ),
    table=dict(
        J=dict(J=R, H=6, L=7, S=8),
        H=dict(J=R, H=4, L=5, S=6),
        L=dict(J=R, H=R, L=R, S=4),
        S=dict(J=R, H=R, L=R, S=R),
    )
)

time_based_separation = dict(
    index=dict(
        leader=True,
        follower=True,
    ),
    table=dict(
        D=dict(
            D=dict(
                H=dict(H=90, L=120, S=120),
                L=dict(H=60, L= 60, S= 60),
                S=dict(H=60, L= 60, S= 60),
            ),
            A=dict(
                H=dict(H=60, L=60, S=60),
                L=dict(H=60, L=60, S=60),
                S=dict(H=60, L=60, S=60),
            ),
        ),
        A=dict(
            D=dict(
                H=dict(H=75, L=75, S=75),
                L=dict(H=75, L=75, S=75),
                S=dict(H=75, L=75, S=75),
            ),
            A=dict(
                H=dict(H=96, L=157, S=196),
                L=dict(H=60, L= 69, S=131),
                S=dict(H=60, L= 69, S= 82),
            ),
        )
    )
)
