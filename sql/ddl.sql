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