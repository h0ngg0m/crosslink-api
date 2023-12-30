create table user
(
    id         bigint auto_increment
        primary key,
    email      varchar(255) not null,
    name       varchar(255) not null,
    auth_type  varchar(255) not null,
    created_at datetime     not null,
    updated_at datetime     not null
) collate = utf8mb4_general_ci;

create table admin
(
    id               bigint auto_increment
        primary key,
    name             varchar(255)  not null,
    login_id         varchar(255)  not null,
    password         varchar(1000) not null,
    authenticated    tinyint(1) not null,
    authenticated_at datetime null,
    role             varchar(255)  not null,
    created_at       datetime      not null,
    updated_at       datetime      not null
) collate = utf8mb4_general_ci;

create table box
(
    id          bigint auto_increment
        primary key,
    name        varchar(255)  not null,
    description text          not null,
    address     varchar(1000) not null,
    city        varchar(255)  not null,
    tel         varchar(255)  not null,
    created_at  datetime      not null,
    updated_at  datetime      not null
) collate = utf8mb4_general_ci;