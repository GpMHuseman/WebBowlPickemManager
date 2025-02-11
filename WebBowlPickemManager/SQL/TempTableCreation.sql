--create table dbo.Team (
--	TeamIdentifier bigint IDENTITY(1, 1) primary key,
--	TeamName varchar(25) not null,
--	CurrentPoints int,
--	MaxPoints int,
--	YearPlaying int not null
--	)

--create table dbo.TeamPick (
--	PickIdentifier bigint IDENTITY(1, 1) primary key,
--	TeamIdentifier bigint foreign key REFERENCES dbo.Team(TeamIdentifier),
--	GameNumber int not null,
--	TeamSelection varchar(50) not null,
--	PointValue int not null,
--	IsCorrect bit
--	)

--create table dbo.Matchups (
--	MatchupIdentifier bigint IDENTITY(1,1) primary key,
--	GameNumber int not null,
--	TeamOne varchar(25) not null,
--	TeamTwo varchar(25) not null,
--	Winner varchar(25),
--	YearPlaying int
--	)

----drop table dbo.TeamPick
----drop table dbo.Team
--select * from dbo.Team
--insert into dbo.Team (TeamName, CurrentPoints, MaxPoints, YearPlaying) values ('Mike SQL Insert', 0, 820, 2024)
--insert into dbo.TeamPick (TeamIdentifier, GameNumber, TeamSelection, PointValue,IsCorrect) values (1, 1, 'Iowa', 40, 0)
--insert into dbo.TeamPick (TeamIdentifier, GameNumber, TeamSelection, PointValue,IsCorrect) values (1, 2, 'SMU', 39, 0)
--insert into dbo.Matchups (GameNumber, TeamOne, TeamTwo, YearPlaying) values (1, 'Iowa', 'Missouri', 2024)
--insert into dbo.Matchups (GameNumber, TeamOne, TeamTwo, YearPlaying) values (2, 'BYU', 'SMU', 2024)

select * from dbo.Team t
inner join dbo.TeamPick tp
	on t.TeamIdentifier = tp.TeamIdentifier
where t.YearPlaying = 2024

select * from dbo.Matchups