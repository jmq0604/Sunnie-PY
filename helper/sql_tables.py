import globals, config

globals.sql_commands = [
    """CREATE TABLE IF NOT EXISTS servers (
        id integer PRIMARY KEY NOT NULL,
        prefix text NOT NULL DEFAULT '{prefix}'
    );""".format(prefix=config.prefix),

    """CREATE TABLE IF NOT EXISTS user_info (
        id integer PRIMARY KEY NOT NULL
    );""",

    """CREATE TABLE IF NOT EXISTS users (
        id integer PRIMARY KEY NOT NULL,
        shop_name text NOT NULL DEFAULT 'Sunnie Pizza',
        slogan text NOT NULL DEFAULT 'None',
        location text NOT NULL DEFAULT 'beach',
        cash integer NOT NULL DEFAULT 7500,
        revenue integer NOT NULL DEFAULT 500,
        total_sold integer NOT NULL DEFAULT 0,
        level integer NOT NULL DEFAULT 0,
        clean_time integer NOT NULL DEFAULT 0,
        daily_time integer NOT NULL DEFAULT 0,
        daily integer NOT NULL DEFAULT 0,
        revenue_pizza integer NOT NULL DEFAULT 25,
        exp integer NOT NULL DEFAULT 0,
        max_storage integer NOT NULL DEFAULT 300,
        capacity integer NOT NULL DEFAULT 50,
        skill_points integer NOT NULL DEFAULT 0
    );""",

    """CREATE TABLE IF NOT EXISTS votes (
           id integer NOT NULL,
           vote_site text NOT NULL DEFAULT 'None',
           timestamp integer NOT NULL DEFAULT 0
    );""",

    """CREATE TABLE IF NOT EXISTS skills (
           id integer NOT NULL,
           skill_id text NOT NULL DEFAULT 'None',
           points integer NOT NULL DEFAULT 0
    );""",

    """CREATE TABLE IF NOT EXISTS bank (
           id integer NOT NULL,
           bank_id text NOT NULL DEFAULT 'None',
           experience integer NOT NULL DEFAULT 50,
           amount integer NOT NULL DEFAULT 0,
           credit_score integer NOT NULL DEFAULT 1,
           claim integer NOT NULL DEFAULT 0,
           bonus_max integer NOT NULL DEFAULT 0
    );""",

    """CREATE TABLE IF NOT EXISTS boosters (
        id integer NOT NULL,
        item_id text NOT NULL,
        use_time integer NOT NULL,
        end_time integer NOT NULL,
        type text NOT NULL DEFAULT 1,
        amount integer NOT NULL DEFAULT 0
    );""",

    """CREATE TABLE IF NOT EXISTS statistic (
        id integer NOT NULL,
        total_commands integer NOT NULL DEFAULT 0,
        total_daily integer NOT NULL DEFAULT 0,
        total_votes integer NOT NULL DEFAULT 0,
        
        total_income integer NOT NULL DEFAULT 0,
        total_spent integer NOT NULL DEFAULT 0,
        
        total_deposit integer NOT NULL DEFAULT 0,
        total_interest integer NOT NULL DEFAULT 0,
        total_transferred integer NOT NULL DEFAULT 0,
        total_received integer NOT NULL DEFAULT 0,
        
        total_work integer NOT NULL DEFAULT 0,
        total_tips integer NOT NULL DEFAULT 0,
        total_skills integer NOT NULL DEFAULT 0,
        
        total_gambling_commands integer NOT NULL DEFAULT 0,
        total_gambling_won integer NOT NULL DEFAULT 0,
        total_gambling_lost integer NOT NULL DEFAULT 0
    );""",

    """CREATE TABLE IF NOT EXISTS user_inv (
        id integer NOT NULL,
        item_id text NOT NULL,
        amount text NOT NULL DEFAULT 0
    );""",

    """CREATE TABLE IF NOT EXISTS user_employee (
        id integer NOT NULL,
        hire_id text NOT NULL,
        name text NOT NULL,
        cost_hour integer NOT NULL DEFAULT 20,
        cooking integer NOT NULL DEFAULT 0,
        social integer NOT NULL DEFAULT 0,
        teamwork integer NOT NULL DEFAULT 0,
        management integer NOT NULL DEFAULT 0, 
        marketing integer NOT NULL DEFAULT 0, 
        role text NOT NULL DEFAULT 'none', 
        income integer NOT NULL DEFAULT 0
    );""",

    """CREATE TABLE IF NOT EXISTS ingredients (
        id integer NOT NULL,
        ingredients_id text NOT NULL,
        amount integer NOT NULL DEFAULT 0
    );""",

    """CREATE TABLE IF NOT EXISTS pizza (
        id integer NOT NULL,
        pizza_id text NOT NULL
    );""",

    """CREATE TABLE IF NOT EXISTS modules (
        id integer NOT NULL,
        module_id text NOT NULL,
        income integer NOT NULL,
        capacity integer NOT NULL
    );""",

    """CREATE TABLE IF NOT EXISTS upgrades (
        id integer NOT NULL,
        upgrade_id text NOT NULL,
        amount integer NOT NULL DEFAULT 0
    );""",

    """CREATE TABLE IF NOT EXISTS ban_users (
        id integer NOT NULL,
        reason text NOT NULL DEFAULT 'None'
    );""",

    """CREATE TABLE IF NOT EXISTS ban_Servers (
        id integer NOT NULL,
        reason text NOT NULL DEFAULT 'None'
    );""",

    """CREATE TABLE IF NOT EXISTS company (
        tag text PRIMARY KEY NOT NULL,
        owner integer NOT NULL DEFAULT 0,
        company_name text NOT NULL DEFAULT 'Mraz LLC',
        motto text NOT NULL DEFAULT 'None',
        money integer NOT NULL DEFAULT 0,
        income integer NOT NULL DEFAULT 750,
        income_sold integer NOT NULL DEFAULT 40,
        total_sold integer NOT NULL DEFAULT 0,
        capacity integer NOT NULL DEFAULT 20,
        exp integer NOT NULL DEFAULT 50,
        level integer NOT NULL DEFAULT 0,
        max_cap integer NOT NULL DEFAULT 5,
        tax_return integer NOT NULL DEFAULT 0
    );""",

    """CREATE TABLE IF NOT EXISTS com_roles (
        id integer PRIMARY KEY NOT NULL,
        tag text NOT NULL,
        role text NOT NULL DEFAULT 'member'
    );""",

    """CREATE TABLE IF NOT EXISTS com_upgrade (
        tag text NOT NULL,
        upgrade_id text NOT NULL,
        amount integer NOT NULL DEFAULT 0
    );""",

    """CREATE TABLE IF NOT EXISTS com_modules (
           tag text NOT NULL,
           module_id text NOT NULL,
           income integer NOT NULL,
           capacity integer NOT NULL
    );""",

    """CREATE TABLE IF NOT EXISTS settings (
        id integer PRIMARY KEY NOT NULL,
        settings_id text NOT NULL,
        value integer NOT NULL DEFAULT 0
    );""",
]


sql_dic = {
    "item_id": 2,
    "use_time": 3,
    "end_time": 4,
    "type": 5,
    "amount": 4,

    "hire_id": 1,
    "name": 2,
    "cost_hour": 3,
    "cooking": 4,
    "social": 5,
    "teamwork": 6,
    "management": 7,
    "marketing": 8,
    "role": 9,
    "income": 10
}