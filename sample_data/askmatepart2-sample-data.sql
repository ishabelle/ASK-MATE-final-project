--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

ALTER TABLE IF EXISTS ONLY public.question
    DROP CONSTRAINT IF EXISTS pk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer
    DROP CONSTRAINT IF EXISTS pk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer
    DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment
    DROP CONSTRAINT IF EXISTS pk_comment_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment
    DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment
    DROP CONSTRAINT IF EXISTS fk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag
    DROP CONSTRAINT IF EXISTS pk_question_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag
    DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.tag
    DROP CONSTRAINT IF EXISTS pk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag
    DROP CONSTRAINT IF EXISTS fk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.users
    DROP CONSTRAINT IF EXISTS pk_id CASCADE;

DROP TABLE IF EXISTS public.question;
CREATE TABLE question
(
    id              serial NOT NULL,
    user_id         int,
    submission_time timestamp without time zone,
    view_number     integer,
    vote_number     integer,
    title           text,
    message         text,
    image           text
);

DROP TABLE IF EXISTS public.answer;
CREATE TABLE answer
(
    id              serial NOT NULL,
    user_id         int,
    submission_time timestamp without time zone,
    vote_number     integer,
    question_id     integer,
    message         text,
    image           text,
    validation      boolean
);

DROP TABLE IF EXISTS public.comment;
CREATE TABLE comment
(
    id              serial NOT NULL,
    user_id         int,
    question_id     integer,
    answer_id       integer,
    message         text,
    submission_time timestamp without time zone,
    edited_count    integer
);


DROP TABLE IF EXISTS public.question_tag;
CREATE TABLE question_tag
(
    question_id integer NOT NULL,
    tag_id      integer NOT NULL
);

DROP TABLE IF EXISTS public.tag;
CREATE TABLE tag
(
    id   serial NOT NULL,
    name text
);

DROP TABLE IF EXISTS public.users CASCADE;
CREATE TABLE users
(
    id              SERIAL       NOT NULL,
    username        varchar(30)  NOT NULL,
    password        varchar(500) NOT NULL,
    submission_time timestamp without time zone,
    count_questions int,
    count_answers   int,
    count_comments  int,
    reputation      int
);


ALTER TABLE ONLY answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);

ALTER TABLE ONLY question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);

ALTER TABLE ONLY tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer (id);

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question (id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question (id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES tag (id);

ALTER TABLE ONLY users
    ADD CONSTRAINT pk_id PRIMARY KEY (id);

ALTER TABLE answer
    ADD FOREIGN KEY (user_id) REFERENCES users (id);


ALTER TABLE question
    ADD FOREIGN KEY (user_id) REFERENCES users (id);


ALTER TABLE comment
    ADD FOREIGN KEY (user_id) REFERENCES users (id);

INSERT INTO users
VALUES (0, 'ala.ma.kota@gmail.com', '$2b$12$BrKHm1OtgiXYdGQvIprLSeWNWLEnDmokwN4ggHCPxg6V1gpItdcYu',
        '2017-04-28 16:49:00', 2, 0, 0, 0);
INSERT INTO users
VALUES (1, 'jan@kowalski.com', '$2b$12$QuLtBO.JqwjlVNhaMOyQ.e2/rFLLkWQ7yoKtX2PPFwPD4ICpOtXpy', '2019-04-28 16:53:00', 1,
        2, 0, 0);
INSERT INTO users
VALUES (2, 'anna@kowalska.pl', '$2b$12$BrKHm1OtgiXYdGQvIprLSeWNWLEnDmokwN4ggHCPxg6V1gpItdcYu', '2015-05-18 11:21:00', 0,
        2, 0, 0);

INSERT INTO question
VALUES (0, 0, '2017-04-28 08:29:00', 29, 7, 'How to make lists in Python?', 'I am totally new to this, any hints?',
        'https://applover.pl/wp-content/uploads/2020/01/kisspng-python-computer-icons-programming-language-executa-5d0f0aa7c78fb3.0414836115612668558174-768x768.png');
INSERT INTO question
VALUES (1, 2, '2017-04-29 09:19:00', 15, 9, 'Wordpress loading multiple jQuery Versions', 'I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(".myBook").booklet();
I could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.
BUT in my theme i also using jquery via webpack so the loading order is now following:
jquery
booklet
app.js (bundled file with webpack, including jquery)',
        'https://blog.malwarebytes.com/wp-content/uploads/2015/11/wordpress-logo-680x400.png');
INSERT INTO question
VALUES (2, 1, '2017-05-01 10:41:00', 1364, 57, 'Drawing canvas with an image picked with Cordova Camera Plugin',
        'I''m getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I''m on IOS, it throws errors such as cross origin issue, or that I''m trying to use an unknown format.',
        'https://image.freepik.com/free-vector/art-color-palette-with-paintbrush-drawing-tools-isolated-white-background-vector-illustration_1284-2394.jpg');
SELECT pg_catalog.setval('question_id_seq', 2, true);

INSERT INTO answer
VALUES (0, 2, '2017-04-28 16:49:00', 4, 1, 'You need to use brackets: my_list = []', 'https://d2pzhy4sc0lwtr.cloudfront.net/post_images/high_density/177/effa9cd44515344ddb3b9f110b90dc8b.png', true);
INSERT INTO answer
VALUES (1, 0, '2017-04-25 14:42:00', 35, 1, 'Look it up in the Python docs', NULL, true);
INSERT INTO answer
VALUES (2, 1, '2017-09-25 18:43:00', 35, 1, 'I dont know..', NULL, true);
SELECT pg_catalog.setval('answer_id_seq', 2, true);

INSERT INTO comment
VALUES (1, 1, 0, NULL, 'Please clarify the question as it is too vague!', '2017-05-01 05:49:00', 0);
INSERT INTO comment
VALUES (2, 2, NULL, 1, 'I think you could use my_list = list() as well.', '2017-05-02 16:55:00', 0);
SELECT pg_catalog.setval('comment_id_seq', 2, true);

INSERT INTO tag
VALUES (1, 'python');
INSERT INTO tag
VALUES (2, 'sql');
INSERT INTO tag
VALUES (3, 'css');
SELECT pg_catalog.setval('tag_id_seq', 3, true);

INSERT INTO question_tag
VALUES (0, 1);
INSERT INTO question_tag
VALUES (1, 3);
INSERT INTO question_tag
VALUES (2, 2);


