from team import TeamFinder

teams = TeamFinder.find_teams('강원도 횡성군')

for team in teams:
    print(team.name)
    print(team.address)
    print(team.contact_number)
    print(team.job_category)
    print(team.working_time)
    print(team.review_cnt)
    print(team.rate_score)
    print()