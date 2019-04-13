--drop table usr_role cascade
select * from usr_role;

insert into usr_role (id, created_at, created_by, updated_at, last_updated_by, deleted, deleted_by, name, description)
values (nextval(usr_role_id_seq), now(), 'SQL Insert',now(), null, False, null, 'Lekarz', 'Weterynarz');
insert into usr_role (id, created_at, created_by, updated_at, last_updated_by, deleted, deleted_by, name, description)
values (nextval(usr_role_id_seq), now(), 'SQL Insert',now(), null, False, null, 'Stażysta', 'Stażysta');

--drop table usr_user
select * from usr_user;

insert into usr_user (id, created_at, created_by, updated_at, last_updated_by, deleted, deleted_by, login, password, first_name, last_name, science_degree, role_id)
values (nextval(usr_user_id_seq), now(), 'SQL Insert', now(), null, False, null,'Weterynarz1', 'Weterynarz1', 'Adam', 'Nowak', 'doc. med.', 1);