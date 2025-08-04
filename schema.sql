drop table if exists jogo;

#tenha calma ja ajeito aq
create table jogo (
    id integer primary key autoincrement,
    nomepersonagem text not null,
    jogoorigem text not null,
    habilidade text not null
);
