from . import main, locations, shops


routers = [     # list of routers to include in app events
    main.router,
    locations.router,
    shops.router,

]
