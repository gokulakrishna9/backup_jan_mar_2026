-- Generated test data
-- Generated at: 2026-03-23T20:58:55.718824
-- Total records: 467

SET FOREIGN_KEY_CHECKS = 0;

-- ems_user (2 records)
INSERT INTO `ems_user` (`user_id`, `first_name`, `last_name`, `gender`, `date_of_birth`, `email_address`, `user_name`, `encrypted_password`, `phone_number`, `profile_photo`, `is_active`, `is_entity`) VALUES (1, 'Bonnie', 'Ramirez', 'female', '2021-09-16', 'jjohnson@example.com', 'perrygrace', 'o0RKKbBc+w', '720.967.3373', 'Better marriage age drop accept reduce.', 0, 1);
INSERT INTO `ems_user` (`user_id`, `first_name`, `last_name`, `gender`, `date_of_birth`, `email_address`, `user_name`, `encrypted_password`, `phone_number`, `profile_photo`, `is_active`, `is_entity`) VALUES (2, 'Scott', 'Mullins', 'other', '2023-08-06', 'egreene@example.org', 'ronald84', '9ZqYKd8W$d', '974-531-4137x4151', 'Practice career treat stand American thousand.', NULL, 1);

-- ems_user_property_group (2 records)
INSERT INTO `ems_user_property_group` (`group_id`, `group_name`, `group_description`, `user_id`, `is_active`) VALUES (1, 'Kimberly Smith', 'Against care moment teach. Political report just would task west argue. Various nature environment rather.', 1, 0);
INSERT INTO `ems_user_property_group` (`group_id`, `group_name`, `group_description`, `user_id`, `is_active`) VALUES (2, 'Crystal Blake', 'Hear step ball major. Drive story TV boy. Line save arm measure.
Case fly room player. Food everybody on idea. People particularly those scene suddenly term.', 2, 1);

-- ems_user_property (2 records)
INSERT INTO `ems_user_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `user_id`) VALUES (1, 'Ashley Baker', NULL, 'Believe discuss parent.', 'Next for throughout test create several. Everyone travel pick most force. Manager red receive have dream.
Car season program big best public important. Total road kind test at through.', 2, 1);
INSERT INTO `ems_user_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `user_id`) VALUES (2, 'Jessica Yang', 'Tonight tell head.', 'Hit measure story.', 'Street need while future real anything. Unit most sort your as rich activity wonder.
Performance agree international pick family. Professional factor describe.', 2, 2);

-- ems_institution (2 records)
INSERT INTO `ems_institution` (`institution_id`, `name`, `description`, `moto`, `institution_type_id`, `website`, `contact_email`, `contact_phone`, `is_active`, `is_entity`) VALUES (1, 'Teresa Kelly', 'Quality prevent medical center. National how into use perform miss enjoy.
Thing compare rather. Base from book dark. War player so employee.', 'Administration heart what her also.', 613, 'http://graves.com/', 'dowens@example.org', NULL, 1, 0);
INSERT INTO `ems_institution` (`institution_id`, `name`, `description`, `moto`, `institution_type_id`, `website`, `contact_email`, `contact_phone`, `is_active`, `is_entity`) VALUES (2, 'Veronica Thomas', 'Price occur here enter meeting.
Sport address wear week manage story.
Reduce sure son girl account so wonder.', 'Member your western staff sing share.', NULL, 'https://salinas.com/', NULL, '001-291-703-6920x63711', 1, 1);

-- ems_institution_property_group (2 records)
INSERT INTO `ems_institution_property_group` (`group_id`, `group_name`, `group_description`, `institution_id`, `is_active`) VALUES (1, 'Kaitlyn Ferguson', 'Sit law case social as you similar name. Guess pick democratic war role source phone including. Our who community hand almost pick contain couple.', 1, 1);
INSERT INTO `ems_institution_property_group` (`group_id`, `group_name`, `group_description`, `institution_id`, `is_active`) VALUES (2, 'Gary Jones', 'Increase hour eight create. Inside kitchen Mr ever.
Put key fine paper door term. Bit watch go. Dream another person bank soon.', 1, 1);

-- ems_institution_property (2 records)
INSERT INTO `ems_institution_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `institution_id`) VALUES (1, 'Jade Mathis', 'Court however thank cut.', 'Turn focus prevent.', 'Include relate religious store away. Anyone her history position generation speak. Key class with growth.', 2, 2);
INSERT INTO `ems_institution_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `institution_id`) VALUES (2, 'Anna Ortiz', 'Choose final fact know.', 'Hospital not kitchen writer national factor.', 'Last number billion Mr man. Management according remain prove trade finally. They have interview.
Account tell value. President security public force poor pay walk.', 1, 2);

-- ems_candidate_institute_link (5 records)
INSERT INTO `ems_candidate_institute_link` (`link_id`, `user_id`, `institution_id`, `comment`, `status`) VALUES (1, 1, 2, 'Own take type room.', 'Heart high about onto.');
INSERT INTO `ems_candidate_institute_link` (`link_id`, `user_id`, `institution_id`, `comment`, `status`) VALUES (2, 1, 2, 'May contain player discussion high.', 'Actually represent doctor project finish throw.');
INSERT INTO `ems_candidate_institute_link` (`link_id`, `user_id`, `institution_id`, `comment`, `status`) VALUES (3, 1, 2, 'Company investment represent game population unit.', 'Would these government represent.');
INSERT INTO `ems_candidate_institute_link` (`link_id`, `user_id`, `institution_id`, `comment`, `status`) VALUES (4, 1, 2, 'Economic tree fine represent half growth.', 'Enter family unit.');
INSERT INTO `ems_candidate_institute_link` (`link_id`, `user_id`, `institution_id`, `comment`, `status`) VALUES (5, 2, 2, 'Large low word democratic.', NULL);

-- ems_user_institute_property_link (5 records)
INSERT INTO `ems_user_institute_property_link` (`link_id`, `user_id`, `property_id`, `comment`) VALUES (1, 1, 2, 'Right begin seem city.');
INSERT INTO `ems_user_institute_property_link` (`link_id`, `user_id`, `property_id`, `comment`) VALUES (2, 1, 2, 'Likely two accept late she.');
INSERT INTO `ems_user_institute_property_link` (`link_id`, `user_id`, `property_id`, `comment`) VALUES (3, 2, 1, 'Question you wait among drive energy interesting.');
INSERT INTO `ems_user_institute_property_link` (`link_id`, `user_id`, `property_id`, `comment`) VALUES (4, 2, 1, 'Ahead cause direction agency same.');
INSERT INTO `ems_user_institute_property_link` (`link_id`, `user_id`, `property_id`, `comment`) VALUES (5, 2, 1, NULL);

-- ems_course (2 records)
INSERT INTO `ems_course` (`course_id`, `course_name`, `description`, `outcomes`, `course_type_id`, `is_published`, `price`, `duration_weeks`, `institution_id`, `is_entity`) VALUES (1, 'Jennifer Santos', 'Book single act rich fill day. White like give same administration note.', 'Hard those purpose war.', 366, 0, 44552967.92, 652, 2, 1);
INSERT INTO `ems_course` (`course_id`, `course_name`, `description`, `outcomes`, `course_type_id`, `is_published`, `price`, `duration_weeks`, `institution_id`, `is_entity`) VALUES (2, 'John Gonzalez', 'Various which member hundred lawyer. Yeah response market now believe form. Support why plant also around scientist heart.
Strategy represent doctor.', 'Large within maybe position card from.', 930, 1, 38269086.9, 846, 2, NULL);

-- ems_course_property_group (2 records)
INSERT INTO `ems_course_property_group` (`group_id`, `group_name`, `group_description`, `course_id`, `is_active`) VALUES (1, 'Edward Miller', 'Available so candidate event join above Mrs. Fight throw carry raise nature contain. Necessary exactly management away writer.', 2, 0);
INSERT INTO `ems_course_property_group` (`group_id`, `group_name`, `group_description`, `course_id`, `is_active`) VALUES (2, 'Mark Mitchell', 'Central number music least. Hope Mr other.
College night up hotel. Professional foreign item way president analysis camera. Senior consider car better test boy.', 2, 0);

-- ems_course_property (5 records)
INSERT INTO `ems_course_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `course_id`) VALUES (1, 'Patricia Jones', 'Police rich present.', 'Night per maybe.', 'Computer gas ahead large company lead. Compare rest actually discussion south impact onto artist.', 1, 2);
INSERT INTO `ems_course_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `course_id`) VALUES (2, 'Jason Mckenzie', 'Determine six read.', 'Range support dark.', 'Assume always federal political former he option. Fact also camera lay notice baby. Animal scientist media strong radio.
My scene small open. Shoulder wife friend art. Account Mrs win see.', 1, 1);
INSERT INTO `ems_course_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `course_id`) VALUES (3, 'Sarah Williams', 'Around phone pressure set civil.', 'Remain they create.', 'Now government subject also finish discover interesting. Find Mrs child dream.
Account exactly pass school develop summer. Attorney body usually mind.', 1, 1);
INSERT INTO `ems_course_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `course_id`) VALUES (4, 'Brett Wilson', NULL, 'Else matter body.', 'Fear attack fill sing social. Defense early explain beautiful population. Avoid first very enough.', 1, 2);
INSERT INTO `ems_course_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `course_id`) VALUES (5, 'Scott Hernandez', 'Moment tax heavy his.', 'Exactly establish Democrat system send give.', 'Doctor note moment appear southern red send. Teacher since certain arrive or ready.
Leg play great memory side. Particularly from away become person fight.', 2, 1);

-- ems_user_course_link (5 records)
INSERT INTO `ems_user_course_link` (`link_id`, `user_id`, `course_id`, `role`) VALUES (1, 1, 2, 'Offer choice score debate.');
INSERT INTO `ems_user_course_link` (`link_id`, `user_id`, `course_id`, `role`) VALUES (2, 1, 2, 'Democratic tree available story boy personal.');
INSERT INTO `ems_user_course_link` (`link_id`, `user_id`, `course_id`, `role`) VALUES (3, 2, 2, 'Bag few car bring.');
INSERT INTO `ems_user_course_link` (`link_id`, `user_id`, `course_id`, `role`) VALUES (4, 2, 1, 'Lead author girl season also.');
INSERT INTO `ems_user_course_link` (`link_id`, `user_id`, `course_id`, `role`) VALUES (5, 1, 1, NULL);

-- ems_user_course_wishlist (5 records)
INSERT INTO `ems_user_course_wishlist` (`wish_id`, `user_id`, `course_id`, `comment`) VALUES (1, 2, 2, 'Concern change common.');
INSERT INTO `ems_user_course_wishlist` (`wish_id`, `user_id`, `course_id`, `comment`) VALUES (2, 2, 1, 'Possible as three could rise kind.');
INSERT INTO `ems_user_course_wishlist` (`wish_id`, `user_id`, `course_id`, `comment`) VALUES (3, 1, 1, 'You six baby none.');
INSERT INTO `ems_user_course_wishlist` (`wish_id`, `user_id`, `course_id`, `comment`) VALUES (4, 1, 1, 'Out player defense hour.');
INSERT INTO `ems_user_course_wishlist` (`wish_id`, `user_id`, `course_id`, `comment`) VALUES (5, 1, 2, 'Experience keep friend.');

-- ems_user_course_purchase (5 records)
INSERT INTO `ems_user_course_purchase` (`purchase_id`, `user_id`, `course_id`, `comment`, `amount`, `transaction_id`, `purchased_on`) VALUES (1, 1, 2, 'College magazine manage prepare.', 2246882.94, 'Hair newspaper learn.', '2026-01-10T16:22:46');
INSERT INTO `ems_user_course_purchase` (`purchase_id`, `user_id`, `course_id`, `comment`, `amount`, `transaction_id`, `purchased_on`) VALUES (2, 1, 1, 'Resource animal performance keep need whatever.', 54920615.91, 'Trouble half film impact.', '2026-01-08T00:16:51');
INSERT INTO `ems_user_course_purchase` (`purchase_id`, `user_id`, `course_id`, `comment`, `amount`, `transaction_id`, `purchased_on`) VALUES (3, 2, 2, NULL, 48952558.17, 'Mouth term board total main.', '2025-02-10T23:37:04');
INSERT INTO `ems_user_course_purchase` (`purchase_id`, `user_id`, `course_id`, `comment`, `amount`, `transaction_id`, `purchased_on`) VALUES (4, 2, 1, 'Dark born course.', 18960248.11, 'Dinner lawyer there direction give.', '2025-06-25T20:31:55');
INSERT INTO `ems_user_course_purchase` (`purchase_id`, `user_id`, `course_id`, `comment`, `amount`, `transaction_id`, `purchased_on`) VALUES (5, 2, 1, 'Add outside any practice this.', 79726576.68, NULL, '2025-04-11T15:54:14');

-- ems_job_post (2 records)
INSERT INTO `ems_job_post` (`job_post_id`, `job_post_subject`, `job_post_description`, `institution_id`, `location`, `salary_range`, `posted_on`, `expires_on`, `is_active`, `is_entity`) VALUES (1, 'In step little.', 'New main state billion education about little deal. Various field speech assume expect politics. Police discuss never necessary community report.', 2, 'Simply them future save on.', 'Collection audience learn.', '2025-06-16T10:11:36', '2025-04-22T17:16:40', 0, 1);
INSERT INTO `ems_job_post` (`job_post_id`, `job_post_subject`, `job_post_description`, `institution_id`, `location`, `salary_range`, `posted_on`, `expires_on`, `is_active`, `is_entity`) VALUES (2, 'Expert animal use dog town answer.', 'Police meet decade two. Church store reduce. Tend rock week sometimes claim.
Shake too party drug industry garden lose. Treatment trial ahead position. Push before respond finally form majority.', 1, 'Learn its government music if.', 'Cultural cost seem.', '2026-03-02T08:37:01', '2025-01-12T20:35:42', 0, 1);

-- ems_job_post_property_group (2 records)
INSERT INTO `ems_job_post_property_group` (`group_id`, `group_name`, `group_description`, `job_post_id`) VALUES (1, 'Zachary Richards', 'Hear walk nothing. Who begin together state.
And as hot throw near born laugh exist. Side great including. Discover big respond country special.', 1);
INSERT INTO `ems_job_post_property_group` (`group_id`, `group_name`, `group_description`, `job_post_id`) VALUES (2, 'Hunter Hayes', 'Politics woman education improve red. Enjoy turn miss either. Key then fill article whole bank skin remain.
Member whatever summer area back side. Nice fish scene a deep when.', 1);

-- ems_job_post_property (5 records)
INSERT INTO `ems_job_post_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `job_post_id`) VALUES (1, 'Courtney Castro', 'While discuss tonight message.', 'Ready either partner how book quickly.', NULL, 2, 1);
INSERT INTO `ems_job_post_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `job_post_id`) VALUES (2, 'Jenny Franklin', 'May over buy nation too.', 'Mrs newspaper body.', 'Sit pull necessary prove together social. Still evidence with theory society either rich memory. Food want them know.
Agree majority last example often. These better individual cold section up how.', 1, 2);
INSERT INTO `ems_job_post_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `job_post_id`) VALUES (3, 'Shelia Powell', 'Class care arm.', 'Evidence day tend somebody.', 'Top even wrong six. At can late modern claim allow. All light marriage book candidate husband lot.
Sell million even good attack.', 2, 1);
INSERT INTO `ems_job_post_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `job_post_id`) VALUES (4, 'Cassidy Anderson', 'Human site which activity agent director.', 'Approach result production step final coach.', 'Everybody down if man discussion despite officer. Use sense item movie would rock five.', 2, 2);
INSERT INTO `ems_job_post_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `job_post_id`) VALUES (5, 'Sandra Lewis', 'Building particularly every much any.', 'Program story campaign music.', 'Also my nice top run cause information. Mention wrong type structure Mrs.
Food military young house another six bill. From start thousand not manage same art. Let bag federal your feeling.', 2, 2);

-- ems_user_job_post_bookmark (5 records)
INSERT INTO `ems_user_job_post_bookmark` (`bookmark_id`, `user_id`, `job_post_id`, `comment`) VALUES (1, 1, 2, 'Employee know agent fund nor.');
INSERT INTO `ems_user_job_post_bookmark` (`bookmark_id`, `user_id`, `job_post_id`, `comment`) VALUES (2, 2, 1, NULL);
INSERT INTO `ems_user_job_post_bookmark` (`bookmark_id`, `user_id`, `job_post_id`, `comment`) VALUES (3, 2, 1, 'Capital mind audience help bar.');
INSERT INTO `ems_user_job_post_bookmark` (`bookmark_id`, `user_id`, `job_post_id`, `comment`) VALUES (4, 1, 2, 'Help although environment.');
INSERT INTO `ems_user_job_post_bookmark` (`bookmark_id`, `user_id`, `job_post_id`, `comment`) VALUES (5, 1, 1, 'Mention assume civil hotel unit.');

-- ems_job_post_user_bookmark (5 records)
INSERT INTO `ems_job_post_user_bookmark` (`bookmark_id`, `job_post_id`, `user_id`, `comment`) VALUES (1, 1, 1, 'Mr security daughter health resource employee.');
INSERT INTO `ems_job_post_user_bookmark` (`bookmark_id`, `job_post_id`, `user_id`, `comment`) VALUES (2, 2, 2, 'Red approach enjoy why.');
INSERT INTO `ems_job_post_user_bookmark` (`bookmark_id`, `job_post_id`, `user_id`, `comment`) VALUES (3, 2, 2, 'Bad probably stock.');
INSERT INTO `ems_job_post_user_bookmark` (`bookmark_id`, `job_post_id`, `user_id`, `comment`) VALUES (4, 1, 2, 'Page safe million difference left.');
INSERT INTO `ems_job_post_user_bookmark` (`bookmark_id`, `job_post_id`, `user_id`, `comment`) VALUES (5, 2, 2, 'Choice lot likely month coach.');

-- ems_subscription_payment_history (5 records)
INSERT INTO `ems_subscription_payment_history` (`payment_id`, `user_id`, `amount`, `subscription_type`, `transaction_details`, `transaction_reference`, `payment_on`) VALUES (1, 2, 6302827711.65, NULL, '{}', 'Sure machine his.', '2026-02-06T08:49:49');
INSERT INTO `ems_subscription_payment_history` (`payment_id`, `user_id`, `amount`, `subscription_type`, `transaction_details`, `transaction_reference`, `payment_on`) VALUES (2, 2, 2829921743.65, NULL, '{}', 'Either exist throughout continue film suffer.', '2024-12-08T22:23:56');
INSERT INTO `ems_subscription_payment_history` (`payment_id`, `user_id`, `amount`, `subscription_type`, `transaction_details`, `transaction_reference`, `payment_on`) VALUES (3, 1, 3632052703.99, 'When they stuff.', '{}', 'Child reach little see.', '2025-09-18T00:57:28');
INSERT INTO `ems_subscription_payment_history` (`payment_id`, `user_id`, `amount`, `subscription_type`, `transaction_details`, `transaction_reference`, `payment_on`) VALUES (4, 2, 2896234586.57, 'Word health others specific center statement.', '{}', 'Available still mention will growth he.', '2024-07-28T18:20:47');
INSERT INTO `ems_subscription_payment_history` (`payment_id`, `user_id`, `amount`, `subscription_type`, `transaction_details`, `transaction_reference`, `payment_on`) VALUES (5, 1, 868450060.55, 'Especially admit owner red several traditional.', '{}', 'Time reduce full.', '2025-03-08T13:30:04');

-- ems_community (2 records)
INSERT INTO `ems_community` (`community_id`, `institute_id`, `name`, `description`, `group_owner_user_id`, `is_entity`) VALUES (1, 2, 'Kathy Russo', 'Adult agreement blood degree.
East least window local nor fill. Western star need. Town receive result much news.', 2, 0);
INSERT INTO `ems_community` (`community_id`, `institute_id`, `name`, `description`, `group_owner_user_id`, `is_entity`) VALUES (2, 1, 'Amber Boone', 'Tv third send word knowledge. Possible agency finish sense send. Majority full last continue town civil admit night.', 1, 0);

-- ems_community_property_group (2 records)
INSERT INTO `ems_community_property_group` (`group_id`, `group_name`, `group_description`, `community_id`) VALUES (1, 'Eric Estes', 'Adult name especially. Anything why risk agree a trip by.
Someone population country. Way he father little under thus add responsibility. Agency network Mr crime.', 1);
INSERT INTO `ems_community_property_group` (`group_id`, `group_name`, `group_description`, `community_id`) VALUES (2, 'Brenda Ortiz', 'Meeting wide TV career seem develop child. Measure on father generation involve. Eight authority such claim wind. Wrong trip think window.', 2);

-- ems_community_property (2 records)
INSERT INTO `ems_community_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `community_id`) VALUES (1, 'Adrienne Skinner', 'Discover along while fight around couple.', 'Pm ago statement people.', 'Scene team which whether second into agreement they. Production know pattern. Lose stage husband camera people become sure. Baby seat Republican understand.', 2, 1);
INSERT INTO `ems_community_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `community_id`) VALUES (2, 'Amy Long', 'We southern few traditional.', 'Pick religious suddenly common.', NULL, 1, 2);

-- ems_community_user_link (5 records)
INSERT INTO `ems_community_user_link` (`link_id`, `community_id`, `user_id`, `role`, `comment`) VALUES (1, 1, 2, 'Region party skill.', 'Investment reason guess tax.');
INSERT INTO `ems_community_user_link` (`link_id`, `community_id`, `user_id`, `role`, `comment`) VALUES (2, 2, 2, 'Process site can.', 'Hope up Democrat recently.');
INSERT INTO `ems_community_user_link` (`link_id`, `community_id`, `user_id`, `role`, `comment`) VALUES (3, 1, 2, 'Out prove special.', 'Interest professional money manage.');
INSERT INTO `ems_community_user_link` (`link_id`, `community_id`, `user_id`, `role`, `comment`) VALUES (4, 2, 1, NULL, NULL);
INSERT INTO `ems_community_user_link` (`link_id`, `community_id`, `user_id`, `role`, `comment`) VALUES (5, 1, 2, 'Material book owner institution.', 'Most play last.');

-- ems_community_property_user_link (5 records)
INSERT INTO `ems_community_property_user_link` (`link_id`, `community_property_id`, `user_id`, `comment`) VALUES (1, 1, 2, 'Next area spend safe.');
INSERT INTO `ems_community_property_user_link` (`link_id`, `community_property_id`, `user_id`, `comment`) VALUES (2, 2, 2, 'Understand exactly always attorney upon federal.');
INSERT INTO `ems_community_property_user_link` (`link_id`, `community_property_id`, `user_id`, `comment`) VALUES (3, 1, 1, NULL);
INSERT INTO `ems_community_property_user_link` (`link_id`, `community_property_id`, `user_id`, `comment`) VALUES (4, 2, 1, 'Lose where situation.');
INSERT INTO `ems_community_property_user_link` (`link_id`, `community_property_id`, `user_id`, `comment`) VALUES (5, 1, 1, 'Fast success put center.');

-- ems_community_user_post (2 records)
INSERT INTO `ems_community_user_post` (`post_id`, `community_id`, `user_id`, `post`, `is_pinned`) VALUES (1, 2, 2, '{}', 0);
INSERT INTO `ems_community_user_post` (`post_id`, `community_id`, `user_id`, `post`, `is_pinned`) VALUES (2, 2, 1, '{}', NULL);

-- ems_community_post_link (5 records)
INSERT INTO `ems_community_post_link` (`link_id`, `post_id`, `community_id`) VALUES (1, 1, 2);
INSERT INTO `ems_community_post_link` (`link_id`, `post_id`, `community_id`) VALUES (2, 2, 1);
INSERT INTO `ems_community_post_link` (`link_id`, `post_id`, `community_id`) VALUES (3, 1, 2);
INSERT INTO `ems_community_post_link` (`link_id`, `post_id`, `community_id`) VALUES (4, 2, 2);
INSERT INTO `ems_community_post_link` (`link_id`, `post_id`, `community_id`) VALUES (5, 1, 1);

-- ems_post_emogi (2 records)
INSERT INTO `ems_post_emogi` (`emogi_id`, `name`, `description`, `file_location`) VALUES (1, 'Emily Reed', 'Model sea next. Security wall offer. Eight recognize describe camera as number tonight audience.
Perhaps simple environment professional bring trial.', 'Movie class mouth boy every seven.');
INSERT INTO `ems_post_emogi` (`emogi_id`, `name`, `description`, `file_location`) VALUES (2, 'Melody Ray', 'Door financial admit water memory wait option street. Organization likely energy money able specific effect.
Bad example their. Control where old culture cup who list.', 'Operation treat build project.');

-- ems_emogi_post_user_link (5 records)
INSERT INTO `ems_emogi_post_user_link` (`link_id`, `emogi_id`, `post_id`, `user_id`) VALUES (1, 1, 1, 2);
INSERT INTO `ems_emogi_post_user_link` (`link_id`, `emogi_id`, `post_id`, `user_id`) VALUES (2, 2, 2, 2);
INSERT INTO `ems_emogi_post_user_link` (`link_id`, `emogi_id`, `post_id`, `user_id`) VALUES (3, 1, 1, 1);
INSERT INTO `ems_emogi_post_user_link` (`link_id`, `emogi_id`, `post_id`, `user_id`) VALUES (4, 1, 1, 2);
INSERT INTO `ems_emogi_post_user_link` (`link_id`, `emogi_id`, `post_id`, `user_id`) VALUES (5, 2, 1, 1);

-- ems_post_flag (5 records)
INSERT INTO `ems_post_flag` (`flag_id`, `type`, `user_id`, `post_id`, `reason`, `flagged_on`) VALUES (1, 'Respond put reveal develop cell air.', 1, 2, 'Start evening trial painting certain hear.', '2026-01-31T05:38:21');
INSERT INTO `ems_post_flag` (`flag_id`, `type`, `user_id`, `post_id`, `reason`, `flagged_on`) VALUES (2, 'Choose few me response great.', 1, 1, 'Hard us smile pass according.', '2024-09-27T13:19:43');
INSERT INTO `ems_post_flag` (`flag_id`, `type`, `user_id`, `post_id`, `reason`, `flagged_on`) VALUES (3, 'Baby reason give.', 1, 1, 'Second run from environmental.', '2024-09-17T05:20:46');
INSERT INTO `ems_post_flag` (`flag_id`, `type`, `user_id`, `post_id`, `reason`, `flagged_on`) VALUES (4, 'Once cost thank case wear area.', 1, 1, 'Article really believe energy.', '2024-06-21T08:23:08');
INSERT INTO `ems_post_flag` (`flag_id`, `type`, `user_id`, `post_id`, `reason`, `flagged_on`) VALUES (5, 'President wall own ever notice follow.', 2, 2, 'End politics religious.', '2025-03-19T23:15:23');

-- ems_post_comment (2 records)
INSERT INTO `ems_post_comment` (`comment_id`, `post_id`, `comment`, `user_id`) VALUES (1, 2, 'Allow agent feel.', 2);
INSERT INTO `ems_post_comment` (`comment_id`, `post_id`, `comment`, `user_id`) VALUES (2, 1, 'Rather rather final drug college property.', 2);

-- ems_post_comment_emogi_link (5 records)
INSERT INTO `ems_post_comment_emogi_link` (`link_id`, `comment_id`, `emogi_id`, `user_id`) VALUES (1, 1, 1, 2);
INSERT INTO `ems_post_comment_emogi_link` (`link_id`, `comment_id`, `emogi_id`, `user_id`) VALUES (2, 1, 2, 1);
INSERT INTO `ems_post_comment_emogi_link` (`link_id`, `comment_id`, `emogi_id`, `user_id`) VALUES (3, 2, 2, 1);
INSERT INTO `ems_post_comment_emogi_link` (`link_id`, `comment_id`, `emogi_id`, `user_id`) VALUES (4, 2, 1, 2);
INSERT INTO `ems_post_comment_emogi_link` (`link_id`, `comment_id`, `emogi_id`, `user_id`) VALUES (5, 1, 2, 1);

-- ems_ai_user_profile_evaluation_parameter_group (2 records)
INSERT INTO `ems_ai_user_profile_evaluation_parameter_group` (`group_id`, `group_name`, `description`) VALUES (1, 'Lindsay Mason', 'Heart sell able because five region chance set. Once official get direction ground establish story.');
INSERT INTO `ems_ai_user_profile_evaluation_parameter_group` (`group_id`, `group_name`, `description`) VALUES (2, 'Catherine Hernandez', NULL);

-- ems_ai_user_profile_evaluation_parameter (5 records)
INSERT INTO `ems_ai_user_profile_evaluation_parameter` (`parameter_id`, `parameter_name`, `group_id`, `parameter_value`) VALUES (1, 'Kristin Reyes', 2, '{}');
INSERT INTO `ems_ai_user_profile_evaluation_parameter` (`parameter_id`, `parameter_name`, `group_id`, `parameter_value`) VALUES (2, 'Sherry Hernandez', 1, '{}');
INSERT INTO `ems_ai_user_profile_evaluation_parameter` (`parameter_id`, `parameter_name`, `group_id`, `parameter_value`) VALUES (3, 'Cathy Ellis', 2, '{}');
INSERT INTO `ems_ai_user_profile_evaluation_parameter` (`parameter_id`, `parameter_name`, `group_id`, `parameter_value`) VALUES (4, 'Mark Nelson', 2, '{}');
INSERT INTO `ems_ai_user_profile_evaluation_parameter` (`parameter_id`, `parameter_name`, `group_id`, `parameter_value`) VALUES (5, 'Julie Clark', 1, '{}');

-- ems_ai_user_profile_evaluation (5 records)
INSERT INTO `ems_ai_user_profile_evaluation` (`evaluation_id`, `user_id`, `property_id`, `evaluation_summary`, `rating`) VALUES (1, 1, 1, NULL, 3.54);
INSERT INTO `ems_ai_user_profile_evaluation` (`evaluation_id`, `user_id`, `property_id`, `evaluation_summary`, `rating`) VALUES (2, 2, 2, '{}', 4.5);
INSERT INTO `ems_ai_user_profile_evaluation` (`evaluation_id`, `user_id`, `property_id`, `evaluation_summary`, `rating`) VALUES (3, 2, 1, '{}', 3.08);
INSERT INTO `ems_ai_user_profile_evaluation` (`evaluation_id`, `user_id`, `property_id`, `evaluation_summary`, `rating`) VALUES (4, 2, 1, '{}', 2.12);
INSERT INTO `ems_ai_user_profile_evaluation` (`evaluation_id`, `user_id`, `property_id`, `evaluation_summary`, `rating`) VALUES (5, 2, 2, '{}', 1.55);

-- ems_ai_evaluation_parameter_group (2 records)
INSERT INTO `ems_ai_evaluation_parameter_group` (`group_id`, `group_name`, `description`) VALUES (1, 'Michael Wells', 'Check oil five live with least. From loss keep create company example. Fact impact book young yourself fine. Become bag hand probably song free.');
INSERT INTO `ems_ai_evaluation_parameter_group` (`group_id`, `group_name`, `description`) VALUES (2, 'Jordan Phelps', 'Word several seat experience minute campaign she.
World able both. City whether no. High station office development. Sense station author after natural clearly.');

-- ems_ai_evaluation_parameter (5 records)
INSERT INTO `ems_ai_evaluation_parameter` (`parameter_id`, `parameter_name`, `parameter_group_id`, `parameter_value`) VALUES (1, 'Kayla Pearson', 2, '{}');
INSERT INTO `ems_ai_evaluation_parameter` (`parameter_id`, `parameter_name`, `parameter_group_id`, `parameter_value`) VALUES (2, 'Rebecca Allen', 2, '{}');
INSERT INTO `ems_ai_evaluation_parameter` (`parameter_id`, `parameter_name`, `parameter_group_id`, `parameter_value`) VALUES (3, 'Kim King', 2, '{}');
INSERT INTO `ems_ai_evaluation_parameter` (`parameter_id`, `parameter_name`, `parameter_group_id`, `parameter_value`) VALUES (4, 'Destiny Koch', 2, '{}');
INSERT INTO `ems_ai_evaluation_parameter` (`parameter_id`, `parameter_name`, `parameter_group_id`, `parameter_value`) VALUES (5, 'Vickie Jimenez', 1, '{}');

-- ems_ai_institution_profile_evaluation (5 records)
INSERT INTO `ems_ai_institution_profile_evaluation` (`evaluation_id`, `institution_id`, `evaluation_summary`, `rating`) VALUES (1, 1, '{}', 4.01);
INSERT INTO `ems_ai_institution_profile_evaluation` (`evaluation_id`, `institution_id`, `evaluation_summary`, `rating`) VALUES (2, 1, '{}', 1.82);
INSERT INTO `ems_ai_institution_profile_evaluation` (`evaluation_id`, `institution_id`, `evaluation_summary`, `rating`) VALUES (3, 1, '{}', 3.57);
INSERT INTO `ems_ai_institution_profile_evaluation` (`evaluation_id`, `institution_id`, `evaluation_summary`, `rating`) VALUES (4, 2, '{}', 3.3);
INSERT INTO `ems_ai_institution_profile_evaluation` (`evaluation_id`, `institution_id`, `evaluation_summary`, `rating`) VALUES (5, 1, '{}', 3.5);

-- ems_ai_job_recommendation (5 records)
INSERT INTO `ems_ai_job_recommendation` (`preference_id`, `job_post_id`, `profile_id`, `preference_rating`, `recommendation_summary`) VALUES (1, 2, 25, 3.77, '{}');
INSERT INTO `ems_ai_job_recommendation` (`preference_id`, `job_post_id`, `profile_id`, `preference_rating`, `recommendation_summary`) VALUES (2, 1, 351, 3.13, '{}');
INSERT INTO `ems_ai_job_recommendation` (`preference_id`, `job_post_id`, `profile_id`, `preference_rating`, `recommendation_summary`) VALUES (3, 2, 86, 3.8, '{}');
INSERT INTO `ems_ai_job_recommendation` (`preference_id`, `job_post_id`, `profile_id`, `preference_rating`, `recommendation_summary`) VALUES (4, 1, 359, 2.88, '{}');
INSERT INTO `ems_ai_job_recommendation` (`preference_id`, `job_post_id`, `profile_id`, `preference_rating`, `recommendation_summary`) VALUES (5, 2, 110, 3.03, NULL);

-- ems_ai_community_post_evaluation (5 records)
INSERT INTO `ems_ai_community_post_evaluation` (`evaluation_id`, `post_id`, `evaluation_summary`, `rating`) VALUES (1, 1, '{}', 1.53);
INSERT INTO `ems_ai_community_post_evaluation` (`evaluation_id`, `post_id`, `evaluation_summary`, `rating`) VALUES (2, 2, '{}', 2.01);
INSERT INTO `ems_ai_community_post_evaluation` (`evaluation_id`, `post_id`, `evaluation_summary`, `rating`) VALUES (3, 2, NULL, 4.19);
INSERT INTO `ems_ai_community_post_evaluation` (`evaluation_id`, `post_id`, `evaluation_summary`, `rating`) VALUES (4, 2, '{}', 3.68);
INSERT INTO `ems_ai_community_post_evaluation` (`evaluation_id`, `post_id`, `evaluation_summary`, `rating`) VALUES (5, 2, '{}', 4.52);

-- ems_ai_market_trend_parameter_group (2 records)
INSERT INTO `ems_ai_market_trend_parameter_group` (`group_id`, `group_name`, `description`, `trend_id`) VALUES (1, 'Miranda Vance', 'Suffer spring no worry design per must rise. Painting something board mean kind themselves.
Up move lawyer successful. Mind analysis hundred ten cup hotel when. Design tree however reason wide.', 950);
INSERT INTO `ems_ai_market_trend_parameter_group` (`group_id`, `group_name`, `description`, `trend_id`) VALUES (2, 'Brandy Wright', 'Ahead its view first story eight property serve. Pull occur become. Practice president research.
Of with exactly ask free on. Sport source build cold just. Clear give her so. Cup theory adult send.', 392);

-- ems_ai_market_trend_parameter (5 records)
INSERT INTO `ems_ai_market_trend_parameter` (`parameter_id`, `parameter_name`, `parameter_value`, `group_id`) VALUES (1, 'Cheryl Barry', '{}', 2);
INSERT INTO `ems_ai_market_trend_parameter` (`parameter_id`, `parameter_name`, `parameter_value`, `group_id`) VALUES (2, 'Katie Howell', '{}', 2);
INSERT INTO `ems_ai_market_trend_parameter` (`parameter_id`, `parameter_name`, `parameter_value`, `group_id`) VALUES (3, 'Gary Campbell', '{}', 1);
INSERT INTO `ems_ai_market_trend_parameter` (`parameter_id`, `parameter_name`, `parameter_value`, `group_id`) VALUES (4, 'Karen Johnson', '{}', 1);
INSERT INTO `ems_ai_market_trend_parameter` (`parameter_id`, `parameter_name`, `parameter_value`, `group_id`) VALUES (5, 'Michelle Sharp', '{}', 2);

-- ems_ai_market_trend_property (2 records)
INSERT INTO `ems_ai_market_trend_property` (`trend_id`, `trend_name`, `trend_description`) VALUES (1, 'Maxwell Torres', 'Stay also American white. Even character instead tough political almost.
Power by enter practice military interview. Message itself pressure morning here. Culture bed ever million such them.');
INSERT INTO `ems_ai_market_trend_property` (`trend_id`, `trend_name`, `trend_description`) VALUES (2, 'John Wade', 'Performance state employee world. Lot eye year member make.
Short real third husband. Personal since our miss see.
Arrive film season. Former wonder will color.');

-- ems_user_profile_document (5 records)
INSERT INTO `ems_user_profile_document` (`document_id`, `user_id`, `title`, `document`, `document_type`) VALUES (1, 2, 'Owner majority get week do ball general could', '{}', 'Least glass those ok.');
INSERT INTO `ems_user_profile_document` (`document_id`, `user_id`, `title`, `document`, `document_type`) VALUES (2, 1, 'Theory them unit star hot always south every', '{}', 'Piece usually next stop.');
INSERT INTO `ems_user_profile_document` (`document_id`, `user_id`, `title`, `document`, `document_type`) VALUES (3, 2, 'Explain huge race require raise', '{}', 'Within day performance there answer.');
INSERT INTO `ems_user_profile_document` (`document_id`, `user_id`, `title`, `document`, `document_type`) VALUES (4, 1, 'Mother will for when', '{}', 'Eat day some financial nearly.');
INSERT INTO `ems_user_profile_document` (`document_id`, `user_id`, `title`, `document`, `document_type`) VALUES (5, 2, 'Moment situation fast business', '{}', 'Difficult yourself set use deep believe.');

-- ems_institution_profile_document (5 records)
INSERT INTO `ems_institution_profile_document` (`document_id`, `institution_id`, `title`, `document`, `document_type`) VALUES (1, 1, 'Management why sort old tend', '{}', 'Their include exist full ever religious.');
INSERT INTO `ems_institution_profile_document` (`document_id`, `institution_id`, `title`, `document`, `document_type`) VALUES (2, 1, NULL, '{}', 'Foreign former more season.');
INSERT INTO `ems_institution_profile_document` (`document_id`, `institution_id`, `title`, `document`, `document_type`) VALUES (3, 1, 'Between upon push should across unit drop', '{}', 'Air news late matter six.');
INSERT INTO `ems_institution_profile_document` (`document_id`, `institution_id`, `title`, `document`, `document_type`) VALUES (4, 1, 'Clear drug want if son might', '{}', NULL);
INSERT INTO `ems_institution_profile_document` (`document_id`, `institution_id`, `title`, `document`, `document_type`) VALUES (5, 1, 'Fact subject similar though fact standard', '{}', 'Main subject bring court.');

-- ems_course_document_group (2 records)
INSERT INTO `ems_course_document_group` (`group_id`, `group_name`, `group_description`, `course_id`, `is_active`) VALUES (1, 'Lisa Kennedy', 'Much long soldier. Feel someone research industry create accept enough.
Career hour whatever indeed government. Suggest have apply next want.', 2, 1);
INSERT INTO `ems_course_document_group` (`group_id`, `group_name`, `group_description`, `course_id`, `is_active`) VALUES (2, 'Christopher Jimenez', 'Create especially ago poor seem bit. Democratic popular exist care raise.
Just large than recent a health follow. Over not despite agree. Member wish face talk fund.', 1, 0);

-- ems_course_document (5 records)
INSERT INTO `ems_course_document` (`document_id`, `course_id`, `group_id`, `title`, `document`, `document_type`, `file_name`) VALUES (1, 1, 2, 'Fund before man live remain dream across food', '{}', 'Sit baby vote service thank claim.', 'Jeffrey Montgomery');
INSERT INTO `ems_course_document` (`document_id`, `course_id`, `group_id`, `title`, `document`, `document_type`, `file_name`) VALUES (2, 1, 2, NULL, '{}', 'Arrive and take star.', 'Heather Rush');
INSERT INTO `ems_course_document` (`document_id`, `course_id`, `group_id`, `title`, `document`, `document_type`, `file_name`) VALUES (3, 2, 2, 'Recently trip step consumer evening nearly', '{}', 'Site drug though detail dark be.', 'Matthew Hernandez');
INSERT INTO `ems_course_document` (`document_id`, `course_id`, `group_id`, `title`, `document`, `document_type`, `file_name`) VALUES (4, 1, 1, 'Book yard situation buy of vote always', '{}', 'Magazine movement space camera instead good.', 'Lisa Moreno');
INSERT INTO `ems_course_document` (`document_id`, `course_id`, `group_id`, `title`, `document`, `document_type`, `file_name`) VALUES (5, 1, 2, NULL, '{}', 'Bill walk government imagine than minute.', 'Natalie Martinez');

-- ems_market_trend_document (5 records)
INSERT INTO `ems_market_trend_document` (`document_id`, `trend_id`, `title`, `document`, `document_type`) VALUES (1, 2, 'Happy old hundred yard daughter', '{}', 'Let hospital good particularly.');
INSERT INTO `ems_market_trend_document` (`document_id`, `trend_id`, `title`, `document`, `document_type`) VALUES (2, 1, 'Increase indicate citizen save everybody', '{}', 'Rule art physical particular cup.');
INSERT INTO `ems_market_trend_document` (`document_id`, `trend_id`, `title`, `document`, `document_type`) VALUES (3, 2, 'Name anything play might quality dream enter surface', '{}', 'Style you look per third try.');
INSERT INTO `ems_market_trend_document` (`document_id`, `trend_id`, `title`, `document`, `document_type`) VALUES (4, 2, 'Artist particularly fine daughter successful wonder', '{}', 'Get get president sister bill crime.');
INSERT INTO `ems_market_trend_document` (`document_id`, `trend_id`, `title`, `document`, `document_type`) VALUES (5, 1, 'Party material letter agreement', '{}', 'World exist professor do range tax.');

-- ems_job_post_document (5 records)
INSERT INTO `ems_job_post_document` (`document_id`, `job_post_id`, `title`, `document`, `document_type`, `file_name`) VALUES (1, 1, 'Section fish there serve our', '{}', 'Force course give provide.', 'Mario Fernandez');
INSERT INTO `ems_job_post_document` (`document_id`, `job_post_id`, `title`, `document`, `document_type`, `file_name`) VALUES (2, 2, 'Tough positive because blue', '{}', NULL, 'William Mahoney');
INSERT INTO `ems_job_post_document` (`document_id`, `job_post_id`, `title`, `document`, `document_type`, `file_name`) VALUES (3, 1, 'Understand theory get movement really stay become', '{}', 'Bring simply garden him officer.', 'Tina White');
INSERT INTO `ems_job_post_document` (`document_id`, `job_post_id`, `title`, `document`, `document_type`, `file_name`) VALUES (4, 1, 'Really keep piece long outside bring big', '{}', 'Small list perform over energy.', 'Amy Smith');
INSERT INTO `ems_job_post_document` (`document_id`, `job_post_id`, `title`, `document`, `document_type`, `file_name`) VALUES (5, 2, 'Arrive must allow itself parent along left action', '{}', 'Medical maybe product head.', NULL);

-- ems_user_education (5 records)
INSERT INTO `ems_user_education` (`education_id`, `user_id`, `institution_id`, `degree_type`, `field_of_study`, `specialization`, `start_date`, `end_date`, `grade_gpa`, `is_verified`, `certificate_document_id`) VALUES (1, 1, 2, 'Area writer wonder health.', 'For north drive will.', 'Order say way story former.', '2022-01-21', '2022-02-01', 'Ahead prevent series see short.', 0, NULL);
INSERT INTO `ems_user_education` (`education_id`, `user_id`, `institution_id`, `degree_type`, `field_of_study`, `specialization`, `start_date`, `end_date`, `grade_gpa`, `is_verified`, `certificate_document_id`) VALUES (2, 1, 2, 'Town step eight Congress account enter.', 'Design act involve push.', 'Yeah summer fear seem teacher.', '2025-09-16', NULL, 'Whole author world arrive month adult.', 0, 210);
INSERT INTO `ems_user_education` (`education_id`, `user_id`, `institution_id`, `degree_type`, `field_of_study`, `specialization`, `start_date`, `end_date`, `grade_gpa`, `is_verified`, `certificate_document_id`) VALUES (3, 1, 2, 'Student state be.', 'Relate both message religious why recently.', NULL, '2023-01-21', NULL, 'Fine without book member move.', 0, 806);
INSERT INTO `ems_user_education` (`education_id`, `user_id`, `institution_id`, `degree_type`, `field_of_study`, `specialization`, `start_date`, `end_date`, `grade_gpa`, `is_verified`, `certificate_document_id`) VALUES (4, 2, 1, 'Try catch join they.', 'Help fall prevent simple.', 'Six phone when.', '2022-04-26', '2022-10-02', NULL, 1, 248);
INSERT INTO `ems_user_education` (`education_id`, `user_id`, `institution_id`, `degree_type`, `field_of_study`, `specialization`, `start_date`, `end_date`, `grade_gpa`, `is_verified`, `certificate_document_id`) VALUES (5, 1, 2, 'Management age fine night common.', 'Someone interest after reach.', 'Arrive happen section different size lay.', '2024-08-22', '2022-04-17', 'See simply agree measure stuff.', NULL, 901);

-- ems_user_work_experience (5 records)
INSERT INTO `ems_user_work_experience` (`experience_id`, `user_id`, `institution_id`, `job_title`, `company_name`, `employment_type`, `location`, `start_date`, `end_date`, `is_current`, `responsibilities`, `achievements`, `skills_used`) VALUES (1, 1, 2, 'Design use trouble', 'Sarah Chan', 'Part-time', 'Base real perform.', '2023-08-04', NULL, 1, 'Possible ability above alone.', 'Expect know science.', '{}');
INSERT INTO `ems_user_work_experience` (`experience_id`, `user_id`, `institution_id`, `job_title`, `company_name`, `employment_type`, `location`, `start_date`, `end_date`, `is_current`, `responsibilities`, `achievements`, `skills_used`) VALUES (2, 1, 1, 'Happy hundred feel people', 'Michael Martin', 'Part-time', 'Out could among account manage.', '2022-08-07', '2023-07-05', 0, 'Huge community arm less.', 'Newspaper reason hit southern.', '{}');
INSERT INTO `ems_user_work_experience` (`experience_id`, `user_id`, `institution_id`, `job_title`, `company_name`, `employment_type`, `location`, `start_date`, `end_date`, `is_current`, `responsibilities`, `achievements`, `skills_used`) VALUES (3, 2, 2, 'Car bar service lawyer order often smile lose', 'Elizabeth Jones', 'Freelance', 'Near face decade discussion.', '2021-09-03', '2023-10-11', 1, NULL, 'Though him government simply stay.', '{}');
INSERT INTO `ems_user_work_experience` (`experience_id`, `user_id`, `institution_id`, `job_title`, `company_name`, `employment_type`, `location`, `start_date`, `end_date`, `is_current`, `responsibilities`, `achievements`, `skills_used`) VALUES (4, 2, 2, 'Adult pay learn by war scientist certainly', 'Tanya Gonzales', 'Full-time', 'Sound authority recent major drug matter.', '2024-02-05', '2024-07-04', 0, 'Page reveal anything customer.', 'Participant walk TV environment challenge tough.', '{}');
INSERT INTO `ems_user_work_experience` (`experience_id`, `user_id`, `institution_id`, `job_title`, `company_name`, `employment_type`, `location`, `start_date`, `end_date`, `is_current`, `responsibilities`, `achievements`, `skills_used`) VALUES (5, 2, 1, 'Change them career site friend play woman audience', 'Catherine Robertson', 'Internship', 'Nearly talk sure although trade else.', '2025-12-18', '2021-09-21', 0, 'Move natural which.', 'Sister feel toward good range.', '{}');

-- ems_user_skill (2 records)
INSERT INTO `ems_user_skill` (`skill_id`, `user_id`, `skill_name`, `skill_category`, `proficiency_level`, `years_of_experience`, `is_verified`, `verified_by_institution_id`, `endorsement_count`) VALUES (1, 1, 'Angel Kline', 'Machine family south already common.', NULL, 643, 0, 1, 287);
INSERT INTO `ems_user_skill` (`skill_id`, `user_id`, `skill_name`, `skill_category`, `proficiency_level`, `years_of_experience`, `is_verified`, `verified_by_institution_id`, `endorsement_count`) VALUES (2, 1, 'Troy Welch', 'Wonder raise administration way.', 'Expert', 90, 0, 1, 79);

-- ems_user_certification (5 records)
INSERT INTO `ems_user_certification` (`certification_id`, `user_id`, `certification_name`, `issuing_organization`, `institution_id`, `issue_date`, `expiry_date`, `credential_id`, `credential_url`, `certificate_document_id`, `is_verified`) VALUES (1, 2, 'Kristy Bailey', 'Martinez-Dunn', 2, '2023-11-06', '2023-11-02', NULL, NULL, 742, 1);
INSERT INTO `ems_user_certification` (`certification_id`, `user_id`, `certification_name`, `issuing_organization`, `institution_id`, `issue_date`, `expiry_date`, `credential_id`, `credential_url`, `certificate_document_id`, `is_verified`) VALUES (2, 2, 'Christopher Cox', 'Brown Inc', 1, '2021-12-07', '2024-09-17', 'Really within this young.', 'http://www.mccarthy.info/', 744, 0);
INSERT INTO `ems_user_certification` (`certification_id`, `user_id`, `certification_name`, `issuing_organization`, `institution_id`, `issue_date`, `expiry_date`, `credential_id`, `credential_url`, `certificate_document_id`, `is_verified`) VALUES (3, 2, 'Bradley Peterson', 'Goodwin-Chen', 1, '2021-03-25', '2023-10-18', NULL, 'http://www.soto-johnson.org/', NULL, 1);
INSERT INTO `ems_user_certification` (`certification_id`, `user_id`, `certification_name`, `issuing_organization`, `institution_id`, `issue_date`, `expiry_date`, `credential_id`, `credential_url`, `certificate_document_id`, `is_verified`) VALUES (4, 1, 'Theresa Morris', 'King, Russell and Edwards', 2, '2024-07-13', '2021-04-19', 'Film before per.', 'https://www.lawson-patton.info/', 144, 1);
INSERT INTO `ems_user_certification` (`certification_id`, `user_id`, `certification_name`, `issuing_organization`, `institution_id`, `issue_date`, `expiry_date`, `credential_id`, `credential_url`, `certificate_document_id`, `is_verified`) VALUES (5, 2, 'Brandon Ward', 'Harris-White', 1, '2023-04-18', '2025-04-06', 'Deal responsibility war want south.', 'https://davis.biz/', 906, 0);

-- ems_user_language (5 records)
INSERT INTO `ems_user_language` (`language_id`, `user_id`, `language_name`, `proficiency_level`, `can_read`, `can_write`, `can_speak`) VALUES (1, 1, 'James Warren', 'Professional', 1, 0, 0);
INSERT INTO `ems_user_language` (`language_id`, `user_id`, `language_name`, `proficiency_level`, `can_read`, `can_write`, `can_speak`) VALUES (2, 2, 'Amy Green', 'Native', 1, 1, 1);
INSERT INTO `ems_user_language` (`language_id`, `user_id`, `language_name`, `proficiency_level`, `can_read`, `can_write`, `can_speak`) VALUES (3, 2, 'Sarah Anderson', 'Professional', 0, 0, 0);
INSERT INTO `ems_user_language` (`language_id`, `user_id`, `language_name`, `proficiency_level`, `can_read`, `can_write`, `can_speak`) VALUES (4, 2, 'Anthony Mcpherson', 'Native', 1, 1, NULL);
INSERT INTO `ems_user_language` (`language_id`, `user_id`, `language_name`, `proficiency_level`, `can_read`, `can_write`, `can_speak`) VALUES (5, 2, 'James Schneider', 'Basic', 0, 1, 1);

-- ems_user_achievement (5 records)
INSERT INTO `ems_user_achievement` (`achievement_id`, `user_id`, `title`, `description`, `achievement_type`, `issuer`, `date_achieved`, `url`, `document_id`) VALUES (1, 1, 'We education such opportunity', 'While movement determine drive seem use. Remember act blood carry government as reflect.', 'Recognize culture move those serious.', 'Animal successful bring human all.', '2023-01-12', 'https://www.bass.com/', 987);
INSERT INTO `ems_user_achievement` (`achievement_id`, `user_id`, `title`, `description`, `achievement_type`, `issuer`, `date_achieved`, `url`, `document_id`) VALUES (2, 2, 'That manage where something every finish', 'Let follow business Democrat study clearly. Population kid own common every century operation.', 'Never prove increase manager.', 'Establish no ball require table term.', '2022-04-13', 'http://www.williams-henderson.com/', 880);
INSERT INTO `ems_user_achievement` (`achievement_id`, `user_id`, `title`, `description`, `achievement_type`, `issuer`, `date_achieved`, `url`, `document_id`) VALUES (3, 1, 'Happen arm black', 'Bag again economy including.
Moment operation compare election save. Collection American during team although hospital coach.', 'Glass final while peace by.', 'Issue eight lot upon.', '2021-07-20', 'https://robertson-taylor.info/', 651);
INSERT INTO `ems_user_achievement` (`achievement_id`, `user_id`, `title`, `description`, `achievement_type`, `issuer`, `date_achieved`, `url`, `document_id`) VALUES (4, 2, 'Agree impact eight wish', NULL, 'Impact design group.', 'His star enough.', '2021-05-05', 'https://www.peterson-cowan.com/', 470);
INSERT INTO `ems_user_achievement` (`achievement_id`, `user_id`, `title`, `description`, `achievement_type`, `issuer`, `date_achieved`, `url`, `document_id`) VALUES (5, 2, 'Whether key agree bar', 'Picture act other note entire finish. Record single forward join provide someone industry. Level floor man green.
Special yeah message. Left week past commercial bed protect.', 'Money common success weight green.', 'Lay chance rock thousand green wait.', '2023-02-13', NULL, NULL);

-- ems_user_social_link (5 records)
INSERT INTO `ems_user_social_link` (`link_id`, `user_id`, `platform`, `profile_url`, `is_verified`) VALUES (1, 1, 'Over own top maybe.', 'https://jackson.net/', 1);
INSERT INTO `ems_user_social_link` (`link_id`, `user_id`, `platform`, `profile_url`, `is_verified`) VALUES (2, 1, 'Into itself air require state.', 'http://www.roberson-young.org/', NULL);
INSERT INTO `ems_user_social_link` (`link_id`, `user_id`, `platform`, `profile_url`, `is_verified`) VALUES (3, 1, 'Film pay guy.', 'https://www.williams-sanders.biz/', 0);
INSERT INTO `ems_user_social_link` (`link_id`, `user_id`, `platform`, `profile_url`, `is_verified`) VALUES (4, 2, 'Room accept forget song next.', 'https://lloyd-wong.info/', 1);
INSERT INTO `ems_user_social_link` (`link_id`, `user_id`, `platform`, `profile_url`, `is_verified`) VALUES (5, 2, 'Need born other control from possible.', 'https://www.austin.com/', 1);

-- ems_institution_department (5 records)
INSERT INTO `ems_institution_department` (`department_id`, `institution_id`, `department_name`, `description`, `head_of_department_user_id`, `contact_email`, `contact_phone`, `is_active`) VALUES (1, 1, 'Robert Olson', 'Whether their defense chance piece operation far. Skill food should by race. Better until eye impact guess quickly opportunity.
Economy house act activity each begin.', 1, 'swang@example.com', '(925)216-5706x8121', 0);
INSERT INTO `ems_institution_department` (`department_id`, `institution_id`, `department_name`, `description`, `head_of_department_user_id`, `contact_email`, `contact_phone`, `is_active`) VALUES (2, 1, 'Richard Snyder', 'Part both particularly. Policy building site despite measure probably brother.
Other include small single painting. Society before upon PM surface.', 1, NULL, '(275)844-5078', 0);
INSERT INTO `ems_institution_department` (`department_id`, `institution_id`, `department_name`, `description`, `head_of_department_user_id`, `contact_email`, `contact_phone`, `is_active`) VALUES (3, 2, 'James Smith', 'Especially establish avoid for onto else there. Nothing director determine success Mr.', 1, 'npitts@example.net', '(922)783-8174x2097', NULL);
INSERT INTO `ems_institution_department` (`department_id`, `institution_id`, `department_name`, `description`, `head_of_department_user_id`, `contact_email`, `contact_phone`, `is_active`) VALUES (4, 1, 'Thomas Short', 'Which mission join entire. Real information response should oil civil away safe.
Four maintain relationship how between. Hospital law especially minute number huge without.', 1, 'alexisgray@example.com', '667.797.0139x0424', 1);
INSERT INTO `ems_institution_department` (`department_id`, `institution_id`, `department_name`, `description`, `head_of_department_user_id`, `contact_email`, `contact_phone`, `is_active`) VALUES (5, 1, 'Carolyn Smith', 'Federal expect glass you three popular. Green baby thing they authority of.
Picture minute idea front. Realize suffer identify notice. Local five able fund always size billion effort.', 1, 'melodywright@example.net', '243-518-4079x7492', 0);

-- ems_institution_location (2 records)
INSERT INTO `ems_institution_location` (`location_id`, `institution_id`, `location_type`, `address_line1`, `address_line2`, `city`, `state_province`, `country`, `postal_code`, `latitude`, `longitude`, `is_primary`) VALUES (1, 2, NULL, 'Notice choose environmental fund.', 'Less newspaper so economic air.', 'Lake Edwintown', 'Colorado', 'Oman', '19986', 82.303126, 103.90014606, 0);
INSERT INTO `ems_institution_location` (`location_id`, `institution_id`, `location_type`, `address_line1`, `address_line2`, `city`, `state_province`, `country`, `postal_code`, `latitude`, `longitude`, `is_primary`) VALUES (2, 2, 'Main Campus', 'Raise probably staff.', 'Face somebody government room.', 'Port Paige', 'North Dakota', 'Brazil', '64198', 97.85992647, 936.3685069, 0);

-- ems_institution_accreditation (5 records)
INSERT INTO `ems_institution_accreditation` (`accreditation_id`, `institution_id`, `accrediting_body`, `accreditation_type`, `accreditation_level`, `issue_date`, `expiry_date`, `certificate_document_id`, `is_active`) VALUES (1, 1, 'Everybody one common need particular box act trip. Scientist hour dark bed.
Each present sometimes kitchen I center modern. Party soon opportunity trouble table responsibility.', 'Group any north call very south.', 'Team kind answer tell ask.', '2024-12-11', '2023-08-12', 846, 1);
INSERT INTO `ems_institution_accreditation` (`accreditation_id`, `institution_id`, `accrediting_body`, `accreditation_type`, `accreditation_level`, `issue_date`, `expiry_date`, `certificate_document_id`, `is_active`) VALUES (2, 1, 'Safe sign foreign attack. Job company among become special. Hear right structure despite your book.
Of agency whatever sense begin nation. Approach suffer any evidence president specific.', 'Smile general above.', 'Pass provide opportunity church year measure.', '2024-03-30', '2022-04-20', 900, 0);
INSERT INTO `ems_institution_accreditation` (`accreditation_id`, `institution_id`, `accrediting_body`, `accreditation_type`, `accreditation_level`, `issue_date`, `expiry_date`, `certificate_document_id`, `is_active`) VALUES (3, 1, 'Herself local read family. Country great recent parent modern senior health. Forward study record above feel thus.
Need director him ago dark record run side. Couple personal believe be happen pattern result. Than foreign article position school drug.', NULL, 'Employee meeting fund ahead along black.', '2023-12-05', '2023-09-24', 243, 1);
INSERT INTO `ems_institution_accreditation` (`accreditation_id`, `institution_id`, `accrediting_body`, `accreditation_type`, `accreditation_level`, `issue_date`, `expiry_date`, `certificate_document_id`, `is_active`) VALUES (4, 2, 'Perform person against once environment. Her start institution clearly pick knowledge high.
Into certainly quite culture whole green management.
Animal job face heart. Couple let fight character green bill. Common ask owner parent accept success ten cut.', 'Religious project daughter local.', NULL, '2026-01-05', '2021-04-01', 387, 1);
INSERT INTO `ems_institution_accreditation` (`accreditation_id`, `institution_id`, `accrediting_body`, `accreditation_type`, `accreditation_level`, `issue_date`, `expiry_date`, `certificate_document_id`, `is_active`) VALUES (5, 1, 'Tree difference discuss tough piece she use nothing. She include month draw give everybody event home. Week chair spend phone benefit student must.
Certain high loss lot. Stand expect long.', 'Information never popular.', 'Drug store discussion bed away.', '2025-09-24', '2024-02-09', 876, 0);

-- ems_institution_ranking (5 records)
INSERT INTO `ems_institution_ranking` (`ranking_id`, `institution_id`, `ranking_organization`, `ranking_year`, `overall_rank`, `country_rank`, `category`, `category_rank`, `score`) VALUES (1, 1, 'Elliott, Harvey and Torres', 983, NULL, 659, 'Space purpose its technology develop.', 679, NULL);
INSERT INTO `ems_institution_ranking` (`ranking_id`, `institution_id`, `ranking_organization`, `ranking_year`, `overall_rank`, `country_rank`, `category`, `category_rank`, `score`) VALUES (2, 1, 'Booth-Martinez', 460, 958, 41, 'Bit single thus significant billion.', NULL, 0.19);
INSERT INTO `ems_institution_ranking` (`ranking_id`, `institution_id`, `ranking_organization`, `ranking_year`, `overall_rank`, `country_rank`, `category`, `category_rank`, `score`) VALUES (3, 2, 'Berg-Arroyo', 520, 343, 946, 'Gun would could save most.', 1000, 0.41);
INSERT INTO `ems_institution_ranking` (`ranking_id`, `institution_id`, `ranking_organization`, `ranking_year`, `overall_rank`, `country_rank`, `category`, `category_rank`, `score`) VALUES (4, 2, 'Johnston Ltd', 644, 719, 381, 'Theory rest traditional should cultural table.', 580, 0.29);
INSERT INTO `ems_institution_ranking` (`ranking_id`, `institution_id`, `ranking_organization`, `ranking_year`, `overall_rank`, `country_rank`, `category`, `category_rank`, `score`) VALUES (5, 2, 'Butler Ltd', 915, 3, NULL, NULL, 177, 0.0);

-- ems_institution_facility (5 records)
INSERT INTO `ems_institution_facility` (`facility_id`, `institution_id`, `facility_name`, `facility_type`, `description`, `capacity`, `location_id`, `is_available`) VALUES (1, 2, 'Mrs. Denise Howell', 'Week each among military should.', NULL, 729, 1, NULL);
INSERT INTO `ems_institution_facility` (`facility_id`, `institution_id`, `facility_name`, `facility_type`, `description`, `capacity`, `location_id`, `is_available`) VALUES (2, 2, 'Crystal Clark', 'Improve teach act image win claim.', NULL, 954, 1, 1);
INSERT INTO `ems_institution_facility` (`facility_id`, `institution_id`, `facility_name`, `facility_type`, `description`, `capacity`, `location_id`, `is_available`) VALUES (3, 2, 'Dawn Mcintosh', 'Cultural analysis smile four dinner along.', NULL, NULL, 1, 1);
INSERT INTO `ems_institution_facility` (`facility_id`, `institution_id`, `facility_name`, `facility_type`, `description`, `capacity`, `location_id`, `is_available`) VALUES (4, 1, 'Joseph Beasley', NULL, 'Image fact with quality. Build various leader against story. Behind woman could represent force.
Degree man society trial prove cost smile.
Day career behind own something glass.', 945, 2, NULL);
INSERT INTO `ems_institution_facility` (`facility_id`, `institution_id`, `facility_name`, `facility_type`, `description`, `capacity`, `location_id`, `is_available`) VALUES (5, 2, 'Brian Lopez', NULL, 'Full rule book coach personal number. Travel receive past college. Process on prepare cell contain nation order prepare.', 832, 2, 0);

-- ems_course_module (2 records)
INSERT INTO `ems_course_module` (`module_id`, `course_id`, `module_name`, `module_number`, `description`, `duration_hours`, `learning_objectives`, `is_mandatory`, `order_sequence`) VALUES (1, 2, 'Dr. Kyle Smith', 324, 'Possible maintain grow lawyer month turn. Beyond each while animal five.
Once last usually tell hour star. Ready hot imagine itself human might.', 917, 'Career detail partner.', NULL, 236);
INSERT INTO `ems_course_module` (`module_id`, `course_id`, `module_name`, `module_number`, `description`, `duration_hours`, `learning_objectives`, `is_mandatory`, `order_sequence`) VALUES (2, 2, 'Patricia Moyer', 462, 'Draw yourself relationship. Everything rest wall yeah him whatever.
Blue occur increase most event director. Few economic in feel. Fly serious stuff marriage list suffer glass.', 511, 'Especially upon Congress.', 1, 200);

-- ems_course_lesson (2 records)
INSERT INTO `ems_course_lesson` (`lesson_id`, `module_id`, `course_id`, `lesson_title`, `lesson_number`, `content_type`, `content_url`, `duration_minutes`, `is_preview_available`, `order_sequence`) VALUES (1, 1, 1, 'Brother arm not commercial turn', 964, 'Text', 'https://www.johnson-clark.com/', 935, 1, 89);
INSERT INTO `ems_course_lesson` (`lesson_id`, `module_id`, `course_id`, `lesson_title`, `lesson_number`, `content_type`, `content_url`, `duration_minutes`, `is_preview_available`, `order_sequence`) VALUES (2, 1, 1, 'Summer home point bit present president', 819, 'Video', 'https://www.thompson-malone.com/', 483, 1, 963);

-- ems_course_prerequisite (5 records)
INSERT INTO `ems_course_prerequisite` (`prerequisite_id`, `course_id`, `prerequisite_course_id`, `prerequisite_type`, `prerequisite_description`, `is_mandatory`) VALUES (1, 1, 2, 'Experience', 'Understand peace avoid feeling up stay significant onto. Hot tough them positive order on write. Have give someone democratic.
No live oil remember. Audience yeah color country sure.', 1);
INSERT INTO `ems_course_prerequisite` (`prerequisite_id`, `course_id`, `prerequisite_course_id`, `prerequisite_type`, `prerequisite_description`, `is_mandatory`) VALUES (2, 1, 2, 'Experience', 'Modern whom they again gun. Often fine character. Yourself structure tree certain order.
Quickly growth decade. Participant environmental magazine behind rule night finish.', 1);
INSERT INTO `ems_course_prerequisite` (`prerequisite_id`, `course_id`, `prerequisite_course_id`, `prerequisite_type`, `prerequisite_description`, `is_mandatory`) VALUES (3, 2, 1, 'Experience', 'House soldier article wide some. Official network stock our.
Team sit during worry. Good word himself item.', 1);
INSERT INTO `ems_course_prerequisite` (`prerequisite_id`, `course_id`, `prerequisite_course_id`, `prerequisite_type`, `prerequisite_description`, `is_mandatory`) VALUES (4, 2, 2, 'Skill', 'Number year traditional positive anything forward. Believe heavy since tend star. Manager degree lead put camera. Physical kind short parent million.', 1);
INSERT INTO `ems_course_prerequisite` (`prerequisite_id`, `course_id`, `prerequisite_course_id`, `prerequisite_type`, `prerequisite_description`, `is_mandatory`) VALUES (5, 1, 1, 'Skill', 'Local son beautiful. I skill bag those special. Third protect rest Mrs.
Forward account thus ability technology detail. Home reveal assume past surface year.', 1);

-- ems_course_instructor (5 records)
INSERT INTO `ems_course_instructor` (`instructor_link_id`, `course_id`, `user_id`, `role`, `bio`, `specialization`) VALUES (1, 1, 2, 'Teaching Assistant', 'I race choose. Think minute customer fire. Well beautiful after me pretty the his.
Money can work parent law trip. House international include gas. Hard action be exist.', 'Conference kitchen source letter school security.');
INSERT INTO `ems_course_instructor` (`instructor_link_id`, `course_id`, `user_id`, `role`, `bio`, `specialization`) VALUES (2, 2, 1, 'Teaching Assistant', 'Strategy business change drive very open range him. Wrong control move father wife explain. Begin far treatment because no.
Might whole his long drug. Herself and camera energy.', 'Between most arm candidate step why.');
INSERT INTO `ems_course_instructor` (`instructor_link_id`, `course_id`, `user_id`, `role`, `bio`, `specialization`) VALUES (3, 1, 2, 'Teaching Assistant', 'Finish participant media none. Them to four less card. Where community be health central.
Interest if bill daughter none. Successful cost visit. Store thought voice involve have.', 'Million Democrat after toward analysis better.');
INSERT INTO `ems_course_instructor` (`instructor_link_id`, `course_id`, `user_id`, `role`, `bio`, `specialization`) VALUES (4, 1, 2, 'Lead Instructor', 'Pattern knowledge event watch local. Response after particular somebody sound find. Anyone certainly dog else.', 'American head to culture.');
INSERT INTO `ems_course_instructor` (`instructor_link_id`, `course_id`, `user_id`, `role`, `bio`, `specialization`) VALUES (5, 2, 2, 'Guest Lecturer', 'Particularly computer indicate officer agreement. Find appear on approach us gas training must.
Reality step may crime. Public major half under. Present speak health scene.', 'Glass response help rest.');

-- ems_course_review (5 records)
INSERT INTO `ems_course_review` (`review_id`, `course_id`, `user_id`, `rating`, `review_title`, `review_text`, `helpful_count`, `is_verified_purchase`) VALUES (1, 1, 1, 2.6, 'Create book executive', 'Large they hot sure company board.', 635, NULL);
INSERT INTO `ems_course_review` (`review_id`, `course_id`, `user_id`, `rating`, `review_title`, `review_text`, `helpful_count`, `is_verified_purchase`) VALUES (2, 2, 2, 1.9, 'Learn should their camera stand', 'Full growth want speech.', 572, 1);
INSERT INTO `ems_course_review` (`review_id`, `course_id`, `user_id`, `rating`, `review_title`, `review_text`, `helpful_count`, `is_verified_purchase`) VALUES (3, 1, 1, 3.8, 'Cost bad culture stand', 'Tend station experience.', 169, 0);
INSERT INTO `ems_course_review` (`review_id`, `course_id`, `user_id`, `rating`, `review_title`, `review_text`, `helpful_count`, `is_verified_purchase`) VALUES (4, 2, 2, 1.9, 'Of single after explain home five', 'Hair service usually.', 456, 0);
INSERT INTO `ems_course_review` (`review_id`, `course_id`, `user_id`, `rating`, `review_title`, `review_text`, `helpful_count`, `is_verified_purchase`) VALUES (5, 2, 1, 4.9, 'Interesting data notice maintain town read', 'Child image run else professional.', 558, 0);

-- ems_course_assignment (2 records)
INSERT INTO `ems_course_assignment` (`assignment_id`, `course_id`, `module_id`, `title`, `description`, `assignment_type`, `max_score`, `passing_score`, `due_date`, `duration_minutes`, `is_mandatory`) VALUES (1, 2, 2, 'Cup hear sing know court war', NULL, 'Essay', 69, 942, '2025-10-27T03:35:11', 339, 1);
INSERT INTO `ems_course_assignment` (`assignment_id`, `course_id`, `module_id`, `title`, `description`, `assignment_type`, `max_score`, `passing_score`, `due_date`, `duration_minutes`, `is_mandatory`) VALUES (2, 2, 1, 'Need decade check season message popular', 'Cause development professional both focus. Member near understand way enter. War recently method.', 'Practical', 745, 724, '2025-05-29T12:17:23', NULL, 0);

-- ems_user_course_progress (5 records)
INSERT INTO `ems_user_course_progress` (`progress_id`, `user_id`, `course_id`, `lesson_id`, `completion_percentage`, `last_accessed_at`, `time_spent_minutes`, `status`) VALUES (1, 1, 2, 2, 290.39, '2024-05-22T10:30:43', 90, 'Not Started');
INSERT INTO `ems_user_course_progress` (`progress_id`, `user_id`, `course_id`, `lesson_id`, `completion_percentage`, `last_accessed_at`, `time_spent_minutes`, `status`) VALUES (2, 2, 1, 1, 916.26, '2025-10-25T19:39:07', 488, 'Dropped');
INSERT INTO `ems_user_course_progress` (`progress_id`, `user_id`, `course_id`, `lesson_id`, `completion_percentage`, `last_accessed_at`, `time_spent_minutes`, `status`) VALUES (3, 1, 2, 1, 315.72, '2024-05-31T04:28:24', 333, NULL);
INSERT INTO `ems_user_course_progress` (`progress_id`, `user_id`, `course_id`, `lesson_id`, `completion_percentage`, `last_accessed_at`, `time_spent_minutes`, `status`) VALUES (4, 1, 2, 1, 811.26, '2024-07-28T17:02:43', 447, 'Completed');
INSERT INTO `ems_user_course_progress` (`progress_id`, `user_id`, `course_id`, `lesson_id`, `completion_percentage`, `last_accessed_at`, `time_spent_minutes`, `status`) VALUES (5, 1, 2, 1, 761.04, '2024-09-25T02:20:51', 284, 'In Progress');

-- ems_user_assignment_submission (5 records)
INSERT INTO `ems_user_assignment_submission` (`submission_id`, `assignment_id`, `user_id`, `submission_content`, `submission_file_id`, `submitted_at`, `score`, `feedback`, `graded_by_user_id`, `graded_at`, `status`) VALUES (1, 2, 2, 'Often according language term inside family. Forward everyone whom few.
House dark although score color tree write hundred. Along edge operation. Go yes adult party back half account. They upon myself treatment attention indicate run.
Page season thank early money. Science available positive market especially simply. Hotel exactly a note door hundred story.', 233, '2025-06-04T10:46:37', 824, 'Cold two son whose low.', 2, '2025-03-07T02:59:52', 'Graded');
INSERT INTO `ems_user_assignment_submission` (`submission_id`, `assignment_id`, `user_id`, `submission_content`, `submission_file_id`, `submitted_at`, `score`, `feedback`, `graded_by_user_id`, `graded_at`, `status`) VALUES (2, 2, 2, 'Likely myself worry market my. Week firm really economy. Contain opportunity free hot knowledge.
Near woman tell seven. Option hear mean vote including.
Whole idea set rich large policy girl. Wait easy president with.
Instead exist open recent bit final.
Six be thus ask hope. Into wide enjoy four. Term another dinner increase that.
How me deal watch. Worker worker others person mind take. These just ability fact.', 258, '2024-08-20T08:21:26', 680, 'Perhaps able leg.', 2, '2025-12-14T00:13:56', 'Submitted');
INSERT INTO `ems_user_assignment_submission` (`submission_id`, `assignment_id`, `user_id`, `submission_content`, `submission_file_id`, `submitted_at`, `score`, `feedback`, `graded_by_user_id`, `graded_at`, `status`) VALUES (3, 2, 2, 'State read thank structure amount. Modern response several heart far cost control.
Involve foreign concern including. Part arrive design if mention.
Back beautiful war ground beat something. Two across free after try focus.
Beyond kind young address guy bad card. Who attorney health rock style impact by.
Tonight PM place child. Ever town similar increase. Religious to cold serious wrong turn.', 947, '2024-05-06T19:18:02', 635, 'Choice common name federal.', 2, NULL, 'Submitted');
INSERT INTO `ems_user_assignment_submission` (`submission_id`, `assignment_id`, `user_id`, `submission_content`, `submission_file_id`, `submitted_at`, `score`, `feedback`, `graded_by_user_id`, `graded_at`, `status`) VALUES (4, 2, 2, 'Science staff sea course central he local. Six art never middle. Because tend series stop religious policy.
Anything range sometimes. Blue seem dog keep.
Provide soldier large new true prepare throw can. Travel rate program letter. Future check wish low create.
Base sing think. Prepare woman door they lay project where. Agency ready apply billion read effect do. Investment issue offer next century first.
Society economic idea staff. Sport impact young identify country many both seek.', 356, '2024-05-27T18:10:07', 801, 'Spend evening TV face.', 1, '2026-01-27T14:25:11', 'Graded');
INSERT INTO `ems_user_assignment_submission` (`submission_id`, `assignment_id`, `user_id`, `submission_content`, `submission_file_id`, `submitted_at`, `score`, `feedback`, `graded_by_user_id`, `graded_at`, `status`) VALUES (5, 2, 2, 'Nation language to north. Near poor six any worker turn establish.
Describe pay young energy. Analysis her finally. East at notice over create. Than list process paper expert program.
That outside writer rather into pretty. Have road area. Before capital get easy.
Situation two surface force four yes. Doctor new after few. Be yeah establish morning resource free statement.
Certain behavior until theory phone manager either. Day cup east new from treatment at. Store international letter.', 720, '2024-05-28T12:44:45', 660, 'Agency raise garden most level staff.', 2, '2025-08-30T01:10:48', 'Resubmit Required');

-- ems_job_post_requirement (5 records)
INSERT INTO `ems_job_post_requirement` (`requirement_id`, `job_post_id`, `requirement_type`, `requirement_description`, `is_mandatory`, `minimum_years`, `proficiency_level`) VALUES (1, 1, 'Language', 'Happy practice ability yard management notice several newspaper. Mr join present common break.', 1, 958, 'Wait west employee sit lose.');
INSERT INTO `ems_job_post_requirement` (`requirement_id`, `job_post_id`, `requirement_type`, `requirement_description`, `is_mandatory`, `minimum_years`, `proficiency_level`) VALUES (2, 2, 'Language', 'Down able pressure international security billion.
Fall three but. Green trial personal level power require after.', 1, 731, 'Production popular detail know policy.');
INSERT INTO `ems_job_post_requirement` (`requirement_id`, `job_post_id`, `requirement_type`, `requirement_description`, `is_mandatory`, `minimum_years`, `proficiency_level`) VALUES (3, 1, 'Language', 'Center also mouth maintain person mouth. Particular I hard top cold. Writer process middle figure deal live.', 1, 836, 'Level your claim.');
INSERT INTO `ems_job_post_requirement` (`requirement_id`, `job_post_id`, `requirement_type`, `requirement_description`, `is_mandatory`, `minimum_years`, `proficiency_level`) VALUES (4, 1, 'Experience', 'Interest concern left rather next necessary. Hot measure small government. Would dog country.
Risk under be appear trial idea painting. Us drop against.
Reason pick nation hold instead share.', 1, NULL, 'Again child one kid.');
INSERT INTO `ems_job_post_requirement` (`requirement_id`, `job_post_id`, `requirement_type`, `requirement_description`, `is_mandatory`, `minimum_years`, `proficiency_level`) VALUES (5, 2, 'Education', 'Level take born.
All little he hold thing early strategy continue. White standard film tough usually. Day rich end something.
Five form center word. Worker table dark nation.', 1, 215, 'Policy among rule.');

-- ems_job_post_benefit (5 records)
INSERT INTO `ems_job_post_benefit` (`benefit_id`, `job_post_id`, `benefit_type`, `benefit_description`) VALUES (1, 2, 'Always half future.', 'Key explain picture PM leave laugh your. Yet everything protect this traditional kind high. Race team such half professional.');
INSERT INTO `ems_job_post_benefit` (`benefit_id`, `job_post_id`, `benefit_type`, `benefit_description`) VALUES (2, 1, 'Data by crime can national life.', 'Second good generation investment Mrs. Now to film place.
Either challenge mouth carry board with majority. When mind morning accept. Think common article scene by six.');
INSERT INTO `ems_job_post_benefit` (`benefit_id`, `job_post_id`, `benefit_type`, `benefit_description`) VALUES (3, 2, 'Call check generation produce way.', NULL);
INSERT INTO `ems_job_post_benefit` (`benefit_id`, `job_post_id`, `benefit_type`, `benefit_description`) VALUES (4, 1, 'Bar property trip one establish situation.', 'Stage maintain without. Mind explain item who authority want represent attack.');
INSERT INTO `ems_job_post_benefit` (`benefit_id`, `job_post_id`, `benefit_type`, `benefit_description`) VALUES (5, 2, 'Outside course notice.', 'Future first find item blood show. Green keep take travel expert glass.');

-- ems_job_application (2 records)
INSERT INTO `ems_job_application` (`application_id`, `job_post_id`, `user_id`, `cover_letter`, `resume_document_id`, `application_status`, `applied_at`, `status_updated_at`, `status_updated_by_user_id`, `notes`) VALUES (1, 2, 1, 'Next character toward.', 2, 'Accepted', '2025-11-26T04:27:48', '2025-10-13T20:23:05', 2, 'Water sense thus.');
INSERT INTO `ems_job_application` (`application_id`, `job_post_id`, `user_id`, `cover_letter`, `resume_document_id`, `application_status`, `applied_at`, `status_updated_at`, `status_updated_by_user_id`, `notes`) VALUES (2, 2, 1, 'Us front improve black any consider.', 638, 'Applied', NULL, '2025-01-18T19:31:29', 2, 'Would tonight child.');

-- ems_job_interview (5 records)
INSERT INTO `ems_job_interview` (`interview_id`, `application_id`, `interview_type`, `interview_round`, `scheduled_at`, `duration_minutes`, `location`, `meeting_link`, `interviewer_user_id`, `status`, `feedback`, `rating`) VALUES (1, 1, 'Final', 827, '2024-04-09T11:09:23', 487, 'Experience hour weight evening red time.', 'Until job man rule himself.', 2, 'Rescheduled', 'War factor support girl.', 3.9);
INSERT INTO `ems_job_interview` (`interview_id`, `application_id`, `interview_type`, `interview_round`, `scheduled_at`, `duration_minutes`, `location`, `meeting_link`, `interviewer_user_id`, `status`, `feedback`, `rating`) VALUES (2, 1, 'Technical', 725, '2025-12-06T08:54:30', 177, 'Law grow same.', NULL, 1, 'Scheduled', 'I page side.', NULL);
INSERT INTO `ems_job_interview` (`interview_id`, `application_id`, `interview_type`, `interview_round`, `scheduled_at`, `duration_minutes`, `location`, `meeting_link`, `interviewer_user_id`, `status`, `feedback`, `rating`) VALUES (3, 2, NULL, 682, '2025-09-28T12:29:27', NULL, 'Site executive window.', 'Building support child show.', 1, 'Rescheduled', 'Set like daughter stop behavior before.', 3.7);
INSERT INTO `ems_job_interview` (`interview_id`, `application_id`, `interview_type`, `interview_round`, `scheduled_at`, `duration_minutes`, `location`, `meeting_link`, `interviewer_user_id`, `status`, `feedback`, `rating`) VALUES (4, 1, NULL, 696, '2024-05-14T12:58:26', 753, 'Compare specific key.', 'Coach wonder on.', 2, 'Rescheduled', 'Wide word court sister car.', 2.3);
INSERT INTO `ems_job_interview` (`interview_id`, `application_id`, `interview_type`, `interview_round`, `scheduled_at`, `duration_minutes`, `location`, `meeting_link`, `interviewer_user_id`, `status`, `feedback`, `rating`) VALUES (5, 1, 'HR', 481, '2024-09-09T21:11:43', 441, 'Assume even growth.', NULL, 2, 'Scheduled', 'Community trial mission provide.', 4.0);

-- ems_job_post_question (2 records)
INSERT INTO `ems_job_post_question` (`question_id`, `job_post_id`, `question_text`, `question_type`, `is_required`, `order_sequence`) VALUES (1, 1, 'Space heavy me day PM individual.', 'Yes/No', 0, 904);
INSERT INTO `ems_job_post_question` (`question_id`, `job_post_id`, `question_text`, `question_type`, `is_required`, `order_sequence`) VALUES (2, 1, 'Training those too answer score.', 'Yes/No', 1, 790);

-- ems_job_application_answer (5 records)
INSERT INTO `ems_job_application_answer` (`answer_id`, `application_id`, `question_id`, `answer_text`, `answer_file_id`) VALUES (1, 2, 1, NULL, 831);
INSERT INTO `ems_job_application_answer` (`answer_id`, `application_id`, `question_id`, `answer_text`, `answer_file_id`) VALUES (2, 2, 1, 'Attorney out heart.', 959);
INSERT INTO `ems_job_application_answer` (`answer_id`, `application_id`, `question_id`, `answer_text`, `answer_file_id`) VALUES (3, 2, 2, 'Close phone light develop small.', NULL);
INSERT INTO `ems_job_application_answer` (`answer_id`, `application_id`, `question_id`, `answer_text`, `answer_file_id`) VALUES (4, 2, 2, 'Partner lawyer record set win.', 870);
INSERT INTO `ems_job_application_answer` (`answer_id`, `application_id`, `question_id`, `answer_text`, `answer_file_id`) VALUES (5, 2, 1, 'Onto effect part activity.', 915);

-- ems_community_category (5 records)
INSERT INTO `ems_community_category` (`category_id`, `community_id`, `category_name`, `description`, `icon`, `color`, `order_sequence`) VALUES (1, 1, 'Jason Turner', 'Attack sea we. Television father always drive thousand answer.
Soldier care remember eight. Write then remain situation. Stand determine those want choice.', 'Seem yet kid customer old also.', 'Citizen trade visit.', 215);
INSERT INTO `ems_community_category` (`category_id`, `community_id`, `category_name`, `description`, `icon`, `color`, `order_sequence`) VALUES (2, 2, 'Heather Olson', 'Live resource poor catch industry thus why. Building traditional usually health suggest cold. Simple president of base.', 'Its expect probably.', 'Energy contain remain.', 50);
INSERT INTO `ems_community_category` (`category_id`, `community_id`, `category_name`, `description`, `icon`, `color`, `order_sequence`) VALUES (3, 2, 'Nicole Velasquez', 'Language maybe soldier move event. Writer detail about off event. Trouble case special tree indeed.
Brother show view. Since painting three answer. Anyone baby as child mean.', 'Unit same audience.', NULL, 486);
INSERT INTO `ems_community_category` (`category_id`, `community_id`, `category_name`, `description`, `icon`, `color`, `order_sequence`) VALUES (4, 2, 'Sherry Jordan', NULL, 'You campaign on action.', NULL, 306);
INSERT INTO `ems_community_category` (`category_id`, `community_id`, `category_name`, `description`, `icon`, `color`, `order_sequence`) VALUES (5, 2, 'Thomas Brown', 'Cell speech son window. Marriage hundred open dark. Father control customer. Anything free require.
Attention identify enter baby.', 'Difference result industry.', 'Expert note hear collection.', 94);

-- ems_community_rule (5 records)
INSERT INTO `ems_community_rule` (`rule_id`, `community_id`, `rule_title`, `rule_description`, `order_sequence`) VALUES (1, 1, 'Whatever realize growth next half', 'Career discuss call reality billion western although. Former room thank article natural somebody approach. Lawyer goal pattern his so. Address stock movie trip.', 718);
INSERT INTO `ems_community_rule` (`rule_id`, `community_id`, `rule_title`, `rule_description`, `order_sequence`) VALUES (2, 2, 'Weight public senior even threat fine fire', 'Seven run big test much out wish.
Difficult young ask even. Her try fund structure economy eye. Part know dark exactly say.', 216);
INSERT INTO `ems_community_rule` (`rule_id`, `community_id`, `rule_title`, `rule_description`, `order_sequence`) VALUES (3, 2, 'From enough point same share statement', 'Important late environmental eat decide person. Citizen everyone day discuss read reveal work drug.
Large answer effect. Charge unit trial list necessary quite.', 615);
INSERT INTO `ems_community_rule` (`rule_id`, `community_id`, `rule_title`, `rule_description`, `order_sequence`) VALUES (4, 2, 'Include technology her white enough', 'Plan near central possible item.
Thought sea situation apply represent. Artist bed human ask boy Mrs support.', 805);
INSERT INTO `ems_community_rule` (`rule_id`, `community_id`, `rule_title`, `rule_description`, `order_sequence`) VALUES (5, 1, 'Population them common already among development', 'Suggest front they trade visit. Thank hand quickly administration economic.
Show several action price rise far. Near maybe card bag something voice on.', 791);

-- ems_community_event (2 records)
INSERT INTO `ems_community_event` (`event_id`, `community_id`, `event_title`, `description`, `event_type`, `start_datetime`, `end_datetime`, `location`, `meeting_link`, `max_attendees`, `organizer_user_id`) VALUES (1, 1, 'Window year environmental', 'Finish executive agent three politics. These lawyer like.
Space air drive get guess tax.
Country item idea provide. Figure action politics including trial attention any onto.', 'Conference', '2025-02-01T20:29:43', '2024-11-12T03:24:20', 'Student wall tax clearly.', 'Exist sell order serve.', 777, 1);
INSERT INTO `ems_community_event` (`event_id`, `community_id`, `event_title`, `description`, `event_type`, `start_datetime`, `end_datetime`, `location`, `meeting_link`, `max_attendees`, `organizer_user_id`) VALUES (2, 2, 'Rule cause hear play use carry', 'Opportunity partner cultural cup laugh consumer language. Measure expert someone member.
Run into letter. Leave bad yourself out create score degree. Whatever goal feeling cost exactly.', 'Webinar', '2025-06-04T22:17:53', '2026-01-01T10:05:45', 'Buy future defense.', NULL, 119, 2);

-- ems_community_event_attendee (5 records)
INSERT INTO `ems_community_event_attendee` (`attendee_id`, `event_id`, `user_id`, `rsvp_status`, `attended`) VALUES (1, 1, 1, 'Maybe', 1);
INSERT INTO `ems_community_event_attendee` (`attendee_id`, `event_id`, `user_id`, `rsvp_status`, `attended`) VALUES (2, 1, 2, 'Going', 0);
INSERT INTO `ems_community_event_attendee` (`attendee_id`, `event_id`, `user_id`, `rsvp_status`, `attended`) VALUES (3, 1, 1, 'Waitlist', 0);
INSERT INTO `ems_community_event_attendee` (`attendee_id`, `event_id`, `user_id`, `rsvp_status`, `attended`) VALUES (4, 1, 2, 'Waitlist', 0);
INSERT INTO `ems_community_event_attendee` (`attendee_id`, `event_id`, `user_id`, `rsvp_status`, `attended`) VALUES (5, 1, 2, 'Going', 1);

-- ems_post_attachment (5 records)
INSERT INTO `ems_post_attachment` (`attachment_id`, `post_id`, `file_name`, `file_type`, `file_url`, `file_size_kb`, `thumbnail_url`) VALUES (1, 2, 'Jennifer Robinson', 'Suggest financial hold.', 'http://www.sheppard.net/', 627, 'http://www.barnes.net/');
INSERT INTO `ems_post_attachment` (`attachment_id`, `post_id`, `file_name`, `file_type`, `file_url`, `file_size_kb`, `thumbnail_url`) VALUES (2, 1, 'Gwendolyn Baker', 'Concern difference point voice student into.', 'https://luna-blankenship.com/', 963, NULL);
INSERT INTO `ems_post_attachment` (`attachment_id`, `post_id`, `file_name`, `file_type`, `file_url`, `file_size_kb`, `thumbnail_url`) VALUES (3, 1, 'Kyle Andrews MD', 'Shake trip with reason four nearly.', 'http://www.dodson.com/', 54, 'http://www.caldwell-sims.com/');
INSERT INTO `ems_post_attachment` (`attachment_id`, `post_id`, `file_name`, `file_type`, `file_url`, `file_size_kb`, `thumbnail_url`) VALUES (4, 1, 'Ronald Allen', NULL, 'https://www.vasquez.com/', NULL, 'https://atkinson.net/');
INSERT INTO `ems_post_attachment` (`attachment_id`, `post_id`, `file_name`, `file_type`, `file_url`, `file_size_kb`, `thumbnail_url`) VALUES (5, 1, 'Kathryn Daniel', 'Start early newspaper the.', 'http://www.lopez.biz/', 501, 'http://www.garcia-holland.org/');

-- ems_post_tag (2 records)
INSERT INTO `ems_post_tag` (`tag_id`, `tag_name`, `description`, `usage_count`) VALUES (1, 'Joyce Castro', 'Design area make smile. Performance treat method after. Health collection pressure would institution teach dark art. Magazine determine image individual material cup across.', 524);
INSERT INTO `ems_post_tag` (`tag_id`, `tag_name`, `description`, `usage_count`) VALUES (2, 'Natasha Lee', 'Art present everybody foreign. Power nor town beautiful interesting commercial develop.
Despite husband compare month. Baby particularly share world doctor together.', 123);

-- ems_post_tag_link (5 records)
INSERT INTO `ems_post_tag_link` (`link_id`, `post_id`, `tag_id`) VALUES (1, 1, 1);
INSERT INTO `ems_post_tag_link` (`link_id`, `post_id`, `tag_id`) VALUES (2, 1, 2);
INSERT INTO `ems_post_tag_link` (`link_id`, `post_id`, `tag_id`) VALUES (3, 1, 2);
INSERT INTO `ems_post_tag_link` (`link_id`, `post_id`, `tag_id`) VALUES (4, 1, 2);
INSERT INTO `ems_post_tag_link` (`link_id`, `post_id`, `tag_id`) VALUES (5, 2, 1);

-- ems_market_trend_skill_demand (5 records)
INSERT INTO `ems_market_trend_skill_demand` (`demand_id`, `trend_id`, `skill_name`, `demand_level`, `growth_rate`, `average_salary_range`, `job_openings_count`, `region`, `industry`) VALUES (1, 1, 'Eric Munoz', 'Very High', 986.21, 'Spring great watch fear.', 123, 'Just strategy that social mention amount.', 'Catch nearly fire senior middle kid.');
INSERT INTO `ems_market_trend_skill_demand` (`demand_id`, `trend_id`, `skill_name`, `demand_level`, `growth_rate`, `average_salary_range`, `job_openings_count`, `region`, `industry`) VALUES (2, 1, 'Kelli Williams', 'Low', 426.79, 'Glass bill task all scientist among.', 413, 'Consumer early around.', 'Wait plan color source test others.');
INSERT INTO `ems_market_trend_skill_demand` (`demand_id`, `trend_id`, `skill_name`, `demand_level`, `growth_rate`, `average_salary_range`, `job_openings_count`, `region`, `industry`) VALUES (3, 2, 'Paula Cervantes', 'Very High', 944.65, NULL, 9, 'Second anything affect key.', 'Wall cold expert.');
INSERT INTO `ems_market_trend_skill_demand` (`demand_id`, `trend_id`, `skill_name`, `demand_level`, `growth_rate`, `average_salary_range`, `job_openings_count`, `region`, `industry`) VALUES (4, 2, 'Corey Wood', 'Medium', 304.94, 'Stop close daughter wish.', 699, 'Claim part oil TV it window.', 'Memory should address support good.');
INSERT INTO `ems_market_trend_skill_demand` (`demand_id`, `trend_id`, `skill_name`, `demand_level`, `growth_rate`, `average_salary_range`, `job_openings_count`, `region`, `industry`) VALUES (5, 1, 'Antonio Becker', 'High', 339.66, 'Sport instead account health.', 884, 'Media father as fine television.', 'Seek government green girl.');

-- ems_market_trend_industry (5 records)
INSERT INTO `ems_market_trend_industry` (`industry_id`, `trend_id`, `industry_name`, `description`, `growth_rate`, `market_size`, `key_players`, `emerging_technologies`) VALUES (1, 1, 'Sarah Shaffer', 'Discuss tax make hard meet majority. Until throughout still thank season box. Manager ability media career hour success job.', 948.82, 'Hand number toward stay.', 'Class away either.', NULL);
INSERT INTO `ems_market_trend_industry` (`industry_id`, `trend_id`, `industry_name`, `description`, `growth_rate`, `market_size`, `key_players`, `emerging_technologies`) VALUES (2, 2, 'Jacqueline Robinson', 'Last already true present pass collection. Space professor agree movie teach.
Option story since. Join anything parent boy.', NULL, 'Rock article easy whatever institution per.', 'Painting decide huge cold your.', 'Development wrong teach.');
INSERT INTO `ems_market_trend_industry` (`industry_id`, `trend_id`, `industry_name`, `description`, `growth_rate`, `market_size`, `key_players`, `emerging_technologies`) VALUES (3, 1, 'Mary Moreno', 'Forget by arm figure event they season. Third upon may teach.
Provide director little well politics attention. Western fight ever tell though. Yourself to compare author magazine.', 116.59, 'Car life enough information industry power.', 'Time thus country act manager doctor.', 'Picture pressure evening card only.');
INSERT INTO `ems_market_trend_industry` (`industry_id`, `trend_id`, `industry_name`, `description`, `growth_rate`, `market_size`, `key_players`, `emerging_technologies`) VALUES (4, 2, 'Gina Gallegos', 'Church voice wrong however. Push chance part charge detail right issue.
Seven store eight skill event away continue. Current democratic long. Across street anyone health what hold bed remember.', 281.36, 'Risk official best shake.', 'Effect off organization trouble true.', 'Accept put measure decade.');
INSERT INTO `ems_market_trend_industry` (`industry_id`, `trend_id`, `industry_name`, `description`, `growth_rate`, `market_size`, `key_players`, `emerging_technologies`) VALUES (5, 2, 'Melissa Hanson', 'With after employee. Write ok we although collection. Wrong left stock build image.
Pull when chair property first always feel. Interview mention manager candidate marriage become provide.', 411.41, 'Hit report particularly thing past large.', 'Send improve wide move.', 'General goal road.');

-- ems_market_trend_location (5 records)
INSERT INTO `ems_market_trend_location` (`location_id`, `trend_id`, `country`, `region`, `city`, `job_market_health`, `unemployment_rate`, `average_salary`, `cost_of_living_index`, `top_industries`) VALUES (1, 1, 'Spain', 'In election forward treat this.', 'West Melissachester', 'Good', 3.77, 'When open necessary.', 819.71, 'Test company offer approach she represent.');
INSERT INTO `ems_market_trend_location` (`location_id`, `trend_id`, `country`, `region`, `city`, `job_market_health`, `unemployment_rate`, `average_salary`, `cost_of_living_index`, `top_industries`) VALUES (2, 1, 'Myanmar', 'Effect region anything others out nation.', 'East Jessica', 'Fair', 905.05, 'Rock wish edge tough share.', 685.31, 'Road thousand own response drive call.');
INSERT INTO `ems_market_trend_location` (`location_id`, `trend_id`, `country`, `region`, `city`, `job_market_health`, `unemployment_rate`, `average_salary`, `cost_of_living_index`, `top_industries`) VALUES (3, 2, 'Mexico', 'Rock pass her hit seat process.', NULL, 'Fair', 663.49, 'Situation upon easy sure let.', 403.62, NULL);
INSERT INTO `ems_market_trend_location` (`location_id`, `trend_id`, `country`, `region`, `city`, `job_market_health`, `unemployment_rate`, `average_salary`, `cost_of_living_index`, `top_industries`) VALUES (4, 2, 'Mexico', 'Why direction us.', NULL, 'Good', 803.45, NULL, 248.05, 'Available discover sister guy back ground.');
INSERT INTO `ems_market_trend_location` (`location_id`, `trend_id`, `country`, `region`, `city`, `job_market_health`, `unemployment_rate`, `average_salary`, `cost_of_living_index`, `top_industries`) VALUES (5, 1, 'Zambia', NULL, 'North Lindsey', 'Good', 792.26, 'Skill off either company.', NULL, 'You focus peace.');

-- ems_user_skill_endorsement (5 records)
INSERT INTO `ems_user_skill_endorsement` (`endorsement_id`, `skill_id`, `endorsed_by_user_id`, `endorsement_comment`, `relationship`) VALUES (1, 2, 2, NULL, 'Card easy cultural author hundred.');
INSERT INTO `ems_user_skill_endorsement` (`endorsement_id`, `skill_id`, `endorsed_by_user_id`, `endorsement_comment`, `relationship`) VALUES (2, 1, 1, 'Yourself discussion any.', 'Exist oil theory tough.');
INSERT INTO `ems_user_skill_endorsement` (`endorsement_id`, `skill_id`, `endorsed_by_user_id`, `endorsement_comment`, `relationship`) VALUES (3, 2, 2, 'Base choose her anyone partner could.', 'Ground fall will.');
INSERT INTO `ems_user_skill_endorsement` (`endorsement_id`, `skill_id`, `endorsed_by_user_id`, `endorsement_comment`, `relationship`) VALUES (4, 2, 1, 'Simple area just season strategy.', 'Meet successful movie hit sport.');
INSERT INTO `ems_user_skill_endorsement` (`endorsement_id`, `skill_id`, `endorsed_by_user_id`, `endorsement_comment`, `relationship`) VALUES (5, 1, 2, 'Think data yet news like probably.', 'Quickly attorney generation style rest.');

-- ems_user_recommendation (5 records)
INSERT INTO `ems_user_recommendation` (`recommendation_id`, `user_id`, `recommended_by_user_id`, `recommendation_text`, `relationship`, `position_at_time`, `is_visible`) VALUES (1, 2, 1, 'Girl drug dinner art live.', 'Turn level certain Republican run.', 'Role marriage pay short amount.', 0);
INSERT INTO `ems_user_recommendation` (`recommendation_id`, `user_id`, `recommended_by_user_id`, `recommendation_text`, `relationship`, `position_at_time`, `is_visible`) VALUES (2, 2, 1, 'Behind continue arm she process building.', 'Late all debate future certainly.', 'Order beautiful thought most later.', 0);
INSERT INTO `ems_user_recommendation` (`recommendation_id`, `user_id`, `recommended_by_user_id`, `recommendation_text`, `relationship`, `position_at_time`, `is_visible`) VALUES (3, 1, 1, 'Line important prepare the save model.', 'Law sister suddenly from.', 'Another company free.', 0);
INSERT INTO `ems_user_recommendation` (`recommendation_id`, `user_id`, `recommended_by_user_id`, `recommendation_text`, `relationship`, `position_at_time`, `is_visible`) VALUES (4, 1, 1, 'Third energy red.', 'Court win benefit rate.', 'But student surface civil.', 1);
INSERT INTO `ems_user_recommendation` (`recommendation_id`, `user_id`, `recommended_by_user_id`, `recommendation_text`, `relationship`, `position_at_time`, `is_visible`) VALUES (5, 2, 1, 'Per inside these night.', 'Return that that.', 'She wide realize responsibility step stage.', 0);

-- ems_notification (5 records)
INSERT INTO `ems_notification` (`notification_id`, `user_id`, `notification_type`, `title`, `message`, `related_entity_type`, `related_entity_id`, `action_url`, `is_read`, `read_at`, `priority`) VALUES (1, 1, 'Keep long say.', 'Far education lawyer oil', 'Military recent eye make energy southern.', 'Lead process year school laugh.', 421, 'http://buchanan.org/', 0, '2024-07-21T22:03:11', 'Low');
INSERT INTO `ems_notification` (`notification_id`, `user_id`, `notification_type`, `title`, `message`, `related_entity_type`, `related_entity_id`, `action_url`, `is_read`, `read_at`, `priority`) VALUES (2, 1, 'Power analysis system.', 'Scientist soon poor heart store', 'Particular job experience the.', 'Spend able music.', 542, 'https://www.anderson.com/', 0, '2024-05-07T08:51:05', 'Normal');
INSERT INTO `ems_notification` (`notification_id`, `user_id`, `notification_type`, `title`, `message`, `related_entity_type`, `related_entity_id`, `action_url`, `is_read`, `read_at`, `priority`) VALUES (3, 2, 'Economy play ahead good join.', 'Inside leader move upon form language project', 'Drug government through civil.', 'Price deep involve situation institution relationship.', 788, NULL, 0, '2024-05-20T06:13:43', 'Urgent');
INSERT INTO `ems_notification` (`notification_id`, `user_id`, `notification_type`, `title`, `message`, `related_entity_type`, `related_entity_id`, `action_url`, `is_read`, `read_at`, `priority`) VALUES (4, 1, 'Chance would similar recognize hold.', 'Again rich relationship home else write', 'Trip blood ten for admit agree television.', 'Off event gas become nor ten.', 119, 'https://mills.com/', 0, '2026-01-03T02:55:35', 'Low');
INSERT INTO `ems_notification` (`notification_id`, `user_id`, `notification_type`, `title`, `message`, `related_entity_type`, `related_entity_id`, `action_url`, `is_read`, `read_at`, `priority`) VALUES (5, 2, 'Laugh get situation summer.', 'Degree father hotel kid', 'Weight information whole you.', 'Blood mean lawyer.', 241, 'https://thomas.net/', 1, '2024-09-10T12:45:23', 'Urgent');

-- ems_course_job_post_link (5 records)
INSERT INTO `ems_course_job_post_link` (`link_id`, `course_id`, `job_post_id`, `relevance_score`, `matching_skills`, `ai_generated`) VALUES (1, 1, 1, 0.8, '{}', 0);
INSERT INTO `ems_course_job_post_link` (`link_id`, `course_id`, `job_post_id`, `relevance_score`, `matching_skills`, `ai_generated`) VALUES (2, 2, 1, 0.1, '{}', 0);
INSERT INTO `ems_course_job_post_link` (`link_id`, `course_id`, `job_post_id`, `relevance_score`, `matching_skills`, `ai_generated`) VALUES (3, 2, 2, 0.13, '{}', 1);
INSERT INTO `ems_course_job_post_link` (`link_id`, `course_id`, `job_post_id`, `relevance_score`, `matching_skills`, `ai_generated`) VALUES (4, 2, 2, 0.6, '{}', 1);
INSERT INTO `ems_course_job_post_link` (`link_id`, `course_id`, `job_post_id`, `relevance_score`, `matching_skills`, `ai_generated`) VALUES (5, 1, 2, 0.78, '{}', NULL);

-- ems_course_community_link (5 records)
INSERT INTO `ems_course_community_link` (`link_id`, `course_id`, `community_id`, `link_type`, `is_active`) VALUES (1, 1, 2, 'Study Group', 1);
INSERT INTO `ems_course_community_link` (`link_id`, `course_id`, `community_id`, `link_type`, `is_active`) VALUES (2, 2, 2, 'Alumni', 1);
INSERT INTO `ems_course_community_link` (`link_id`, `course_id`, `community_id`, `link_type`, `is_active`) VALUES (3, 2, 2, 'Discussion', 1);
INSERT INTO `ems_course_community_link` (`link_id`, `course_id`, `community_id`, `link_type`, `is_active`) VALUES (4, 1, 1, 'Study Group', 1);
INSERT INTO `ems_course_community_link` (`link_id`, `course_id`, `community_id`, `link_type`, `is_active`) VALUES (5, 1, 1, 'Alumni', 1);

-- ems_job_post_community_link (5 records)
INSERT INTO `ems_job_post_community_link` (`link_id`, `job_post_id`, `community_id`, `is_featured`, `posted_by_user_id`) VALUES (1, 2, 2, 0, 1);
INSERT INTO `ems_job_post_community_link` (`link_id`, `job_post_id`, `community_id`, `is_featured`, `posted_by_user_id`) VALUES (2, 2, 1, 1, 1);
INSERT INTO `ems_job_post_community_link` (`link_id`, `job_post_id`, `community_id`, `is_featured`, `posted_by_user_id`) VALUES (3, 1, 1, 1, 1);
INSERT INTO `ems_job_post_community_link` (`link_id`, `job_post_id`, `community_id`, `is_featured`, `posted_by_user_id`) VALUES (4, 2, 1, 0, 1);
INSERT INTO `ems_job_post_community_link` (`link_id`, `job_post_id`, `community_id`, `is_featured`, `posted_by_user_id`) VALUES (5, 1, 2, 1, 1);

-- ems_market_trend_course_link (5 records)
INSERT INTO `ems_market_trend_course_link` (`link_id`, `trend_id`, `course_id`, `relevance_score`, `demand_level`, `recommendation_reason`, `ai_generated`) VALUES (1, 1, 1, 0.49, 'Medium', 'Relate stock conference left enjoy.', 0);
INSERT INTO `ems_market_trend_course_link` (`link_id`, `trend_id`, `course_id`, `relevance_score`, `demand_level`, `recommendation_reason`, `ai_generated`) VALUES (2, 2, 2, 0.46, NULL, 'Reflect art over condition total indicate.', 1);
INSERT INTO `ems_market_trend_course_link` (`link_id`, `trend_id`, `course_id`, `relevance_score`, `demand_level`, `recommendation_reason`, `ai_generated`) VALUES (3, 2, 2, 0.83, 'High', 'Cup church pick effect less.', 1);
INSERT INTO `ems_market_trend_course_link` (`link_id`, `trend_id`, `course_id`, `relevance_score`, `demand_level`, `recommendation_reason`, `ai_generated`) VALUES (4, 2, 2, 0.14, 'High', 'Or resource office cover.', 0);
INSERT INTO `ems_market_trend_course_link` (`link_id`, `trend_id`, `course_id`, `relevance_score`, `demand_level`, `recommendation_reason`, `ai_generated`) VALUES (5, 2, 1, 0.01, 'Very High', 'Old big modern certainly short sort.', 1);

-- ems_market_trend_job_post_link (5 records)
INSERT INTO `ems_market_trend_job_post_link` (`link_id`, `trend_id`, `job_post_id`, `relevance_score`, `growth_potential`, `salary_trend`, `ai_generated`) VALUES (1, 1, 1, 0.9, 'Very High', 'West skin brother.', 0);
INSERT INTO `ems_market_trend_job_post_link` (`link_id`, `trend_id`, `job_post_id`, `relevance_score`, `growth_potential`, `salary_trend`, `ai_generated`) VALUES (2, 2, 1, 0.65, 'High', 'Simply for not.', 1);
INSERT INTO `ems_market_trend_job_post_link` (`link_id`, `trend_id`, `job_post_id`, `relevance_score`, `growth_potential`, `salary_trend`, `ai_generated`) VALUES (3, 2, 1, 0.68, 'Low', 'Item sort pay.', 0);
INSERT INTO `ems_market_trend_job_post_link` (`link_id`, `trend_id`, `job_post_id`, `relevance_score`, `growth_potential`, `salary_trend`, `ai_generated`) VALUES (4, 2, 2, 0.65, 'High', NULL, 1);
INSERT INTO `ems_market_trend_job_post_link` (`link_id`, `trend_id`, `job_post_id`, `relevance_score`, `growth_potential`, `salary_trend`, `ai_generated`) VALUES (5, 2, 1, 0.03, 'Low', 'Citizen tree experience.', 1);

-- ems_market_trend_institution_link (5 records)
INSERT INTO `ems_market_trend_institution_link` (`link_id`, `trend_id`, `institution_id`, `relevance_score`, `specialization_areas`, `partnership_opportunities`, `ai_generated`) VALUES (1, 1, 2, 0.28, 'Structure Mrs become thought author who.', 'Job thus spend my top serious.', 1);
INSERT INTO `ems_market_trend_institution_link` (`link_id`, `trend_id`, `institution_id`, `relevance_score`, `specialization_areas`, `partnership_opportunities`, `ai_generated`) VALUES (2, 2, 1, 0.5, 'Popular argue generation weight.', 'World fly get left.', 1);
INSERT INTO `ems_market_trend_institution_link` (`link_id`, `trend_id`, `institution_id`, `relevance_score`, `specialization_areas`, `partnership_opportunities`, `ai_generated`) VALUES (3, 2, 2, 0.78, 'Situation last street travel development author.', 'Activity force rock plan board.', 1);
INSERT INTO `ems_market_trend_institution_link` (`link_id`, `trend_id`, `institution_id`, `relevance_score`, `specialization_areas`, `partnership_opportunities`, `ai_generated`) VALUES (4, 1, 2, NULL, 'Language car state step on traditional.', 'Movement near sometimes fall.', 0);
INSERT INTO `ems_market_trend_institution_link` (`link_id`, `trend_id`, `institution_id`, `relevance_score`, `specialization_areas`, `partnership_opportunities`, `ai_generated`) VALUES (5, 2, 2, 0.47, 'Crime skin huge special good save.', 'Now within economy improve blue peace.', NULL);

-- ems_user_file (5 records)
INSERT INTO `ems_user_file` (`file_id`, `user_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_verified`, `download_count`, `thumbnail_location`) VALUES (1, 1, 'Amy Robertson', 'William Greer', 'pdf', 'Modern some idea his', 'Evening Mrs identify plan wide they.', 734, NULL, 'Our simple learn hotel ago. Pressure their sea myself attention herself.
Impact necessary mean successful answer majority. Wrong face cause. Behind whatever could house college factor.', 'Turn two wonder set think.', NULL, NULL, 479, NULL);
INSERT INTO `ems_user_file` (`file_id`, `user_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_verified`, `download_count`, `thumbnail_location`) VALUES (2, 2, 'Amy Valdez', 'William Young', 'image', 'Institution land sim', 'Forward college color.', 569, 'Fly financial natural program reality you.', 'Ball professor music hold. Today account they recently. Crime best account father place detail buy citizen.
Enough force white difference deep. Care medical ahead Congress edge wonder.', NULL, 'Own only would create.', 1, 33, 'Above fast these drop probably day.');
INSERT INTO `ems_user_file` (`file_id`, `user_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_verified`, `download_count`, `thumbnail_location`) VALUES (3, 1, 'Martin Lewis', 'Rebecca Johnston', 'other', 'Move beat require.', 'Discuss organization idea society.', 991, 'Somebody employee the consider war.', 'Road understand direction author glass college. Send table that take. Oil food history science. Level almost doctor family.
Writer reveal wife indicate indeed into season.', NULL, NULL, 0, 697, 'Part issue at say art news.');
INSERT INTO `ems_user_file` (`file_id`, `user_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_verified`, `download_count`, `thumbnail_location`) VALUES (4, 1, 'Monique Mills', 'Robin Benson', 'html', NULL, 'North also different within shake.', NULL, 'Soon turn matter majority out radio manage.', 'Performance my up environmental fact anyone. Television look policy name. Firm hit professor worry call reason speak.
Of thing region same we. Way land or. Be couple unit land citizen instead.', 'Apply size challenge attorney avoid government.', 'Go tough much.', 1, 77, 'Statement kid allow yard much.');
INSERT INTO `ems_user_file` (`file_id`, `user_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_verified`, `download_count`, `thumbnail_location`) VALUES (5, 2, 'Heather Perez', 'Kara Gomez', 'presentation', NULL, 'Attack everything treat.', NULL, 'Hospital edge above claim.', 'Focus meet anyone serious although. Guy thing message many yeah. Do want quite discuss. Effect boy late determine get have.
Computer learn floor against executive movie or agency. Cell throw why.', 'Tonight stock institution speech wife.', 'Spring involve control act eye.', 1, 185, 'Because growth report employee minute game.');

-- ems_institution_file (5 records)
INSERT INTO `ems_institution_file` (`file_id`, `institution_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_verified`, `download_count`, `thumbnail_location`) VALUES (1, 1, 'Taylor Reyes MD', 'Samantha Dillon', 'other', 'Daughter each discus', 'Add real part visit cell.', 501, 'Today reason quality clearly.', 'Must us everyone nearly possible until spend. During travel first suffer will special. Truth lead focus fill.
Material their others food. Program process quite good he. Upon hair boy.', NULL, 'State director every year man.', 1, 732, 'Cup benefit dream rest.');
INSERT INTO `ems_institution_file` (`file_id`, `institution_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_verified`, `download_count`, `thumbnail_location`) VALUES (2, 1, 'Amanda Lawrence', 'Mariah Melendez', 'code', 'Run nation yeah cult', 'Large from strategy whole yourself.', 504, 'From sell heart store others.', 'Special range trade low off ever husband. Fact want another though under center.
Only wait action woman nice. Himself gun heart do participant recognize.', 'Fill radio reach animal theory.', 'Week politics yet.', 0, 301, 'True word room clearly.');
INSERT INTO `ems_institution_file` (`file_id`, `institution_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_verified`, `download_count`, `thumbnail_location`) VALUES (3, 1, 'Roberto Page', 'Patricia Rodriguez', 'image', 'Head run cold recent', 'Stuff amount personal central.', 258, 'Former thought pretty produce learn theory.', 'Cut color final ten company purpose anything. City series thing when. Modern writer wrong federal appear.', 'Fight few baby kind in.', 'Page onto bit cell soldier process.', 0, 953, 'Purpose close cultural.');
INSERT INTO `ems_institution_file` (`file_id`, `institution_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_verified`, `download_count`, `thumbnail_location`) VALUES (4, 1, 'James Chung', 'William Mcgee', 'html', 'Majority difficult p', 'Yes no audience outside.', 37, 'Season resource east summer company prove.', 'Whom wife child way customer research. While someone election middle gas school. Camera middle decision crime.', 'Three argue soldier may behind history.', NULL, NULL, 998, 'Million he area site of.');
INSERT INTO `ems_institution_file` (`file_id`, `institution_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_verified`, `download_count`, `thumbnail_location`) VALUES (5, 1, 'Ryan Zhang', 'Brandon Foley', 'video', 'Thus return threat.', 'House enter strategy sort field perhaps.', 92, 'Away every marriage recently.', 'Attack finish opportunity believe once. She notice person trip leader. Sell Republican order such language.
Win bring which skin popular room safe. Read exactly win all the month.', 'College eye language.', 'Describe small will only.', 0, 459, 'How well wide finish prove true.');

-- ems_course_file (5 records)
INSERT INTO `ems_course_file` (`file_id`, `course_id`, `module_id`, `lesson_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_downloadable`, `requires_enrollment`, `download_count`, `thumbnail_location`, `duration_seconds`) VALUES (1, 2, 2, 1, 'Rodney Schwartz', 'Kenneth Young', 'presentation', 'Attention option spo', 'Hair blue experience interest.', NULL, 'System friend agree break pretty worry.', 'Test population final take professor. Hand action thought whatever wind.
Beat test effect. Ahead usually thing then budget for major.', 'Big his turn more PM.', 'Evidence laugh natural.', 1, 0, 977, 'Face little side environmental.', 150);
INSERT INTO `ems_course_file` (`file_id`, `course_id`, `module_id`, `lesson_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_downloadable`, `requires_enrollment`, `download_count`, `thumbnail_location`, `duration_seconds`) VALUES (2, 2, 1, 1, 'Deanna Taylor', 'Kevin Chang Jr.', 'code', 'Question system situ', 'Art attack similar.', 54, 'Whole small into help speak.', 'Church bit just service my present. Pass such cause you child learn should. Occur live relationship million industry notice.
Imagine oil behind light hear. End station vote economy.', 'Guess data fish.', 'Especially college both.', 0, 1, NULL, 'Take sea senior.', NULL);
INSERT INTO `ems_course_file` (`file_id`, `course_id`, `module_id`, `lesson_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_downloadable`, `requires_enrollment`, `download_count`, `thumbnail_location`, `duration_seconds`) VALUES (3, 2, 1, 1, 'Drew Page', 'Justin Arnold', 'image', 'History such card as', 'Why evening themselves.', NULL, 'Share process thought discuss protect number.', 'Program black require many. Fly project list contain pay paper. At cold meeting day decide control.', 'So culture party if property.', 'A stand black ball game agent.', 1, NULL, 213, 'Center citizen well thing girl author.', 930);
INSERT INTO `ems_course_file` (`file_id`, `course_id`, `module_id`, `lesson_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_downloadable`, `requires_enrollment`, `download_count`, `thumbnail_location`, `duration_seconds`) VALUES (4, 2, 2, 1, 'Thomas Allen', 'Donna Cervantes', 'other', 'Person nor game teac', 'Between box become.', 460, 'Save action so.', 'Around better identify security professional character gas son. Call put moment play note cause.
Economy identify dinner I discussion. People after focus.', 'Reduce well affect whatever follow.', 'Have throw parent which ok collection.', 0, 0, NULL, 'Travel religious never sense high artist.', NULL);
INSERT INTO `ems_course_file` (`file_id`, `course_id`, `module_id`, `lesson_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_downloadable`, `requires_enrollment`, `download_count`, `thumbnail_location`, `duration_seconds`) VALUES (5, 2, 2, 2, 'Karen Jackson', 'James Sandoval', 'archive', 'Letter goal produce ', 'Can bad development country space week.', 258, 'Successful almost become.', 'Role second expert body.
Research song run job. Your morning he. Eat nothing memory once simply.
Ask laugh true country week issue trial. Finally financial campaign whom.', NULL, NULL, 0, 1, 440, 'Morning let alone American production month.', 102);

-- ems_job_post_file (5 records)
INSERT INTO `ems_job_post_file` (`file_id`, `job_post_id`, `application_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `uploaded_by_user_id`, `download_count`, `thumbnail_location`) VALUES (1, 2, 2, 'Katelyn Larsen', 'Reginald Murray', 'pdf', 'Against within defen', 'Father spend with.', 414, 'Plant lay hour.', 'Of order some night will during both. Reduce laugh wind manager suddenly share.', 'Win member feel manager produce against.', 'Recently hot half end garden.', 2, 997, 'Study history when.');
INSERT INTO `ems_job_post_file` (`file_id`, `job_post_id`, `application_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `uploaded_by_user_id`, `download_count`, `thumbnail_location`) VALUES (2, 2, 1, 'Dawn Burgess', 'Jordan Johnson', 'spreadsheet', NULL, 'Onto teach place bank girl team.', 751, 'Consumer professor ready probably.', 'Race either often reach. Food next recently. Realize enjoy true city.
Media guess type tree. Reflect exactly hair miss. Set cover reflect simple. Three cost view sing provide through huge.', 'Outside artist dinner marriage between any.', 'Factor environment enjoy even.', 1, 534, 'Contain sure likely because sometimes model.');
INSERT INTO `ems_job_post_file` (`file_id`, `job_post_id`, `application_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `uploaded_by_user_id`, `download_count`, `thumbnail_location`) VALUES (3, 1, 2, 'Leslie Davis', 'Kathleen Gutierrez', 'spreadsheet', 'Road form dog perfor', 'Into answer everybody.', 604, 'Identify role future never contain get.', 'Paper control record threat manage drop. Whatever leave effort learn interest with direction. Marriage focus support network tend each voice.', 'Treat note security.', 'Common rich best in yourself.', 1, 836, 'Garden often society many dog.');
INSERT INTO `ems_job_post_file` (`file_id`, `job_post_id`, `application_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `uploaded_by_user_id`, `download_count`, `thumbnail_location`) VALUES (4, 1, 1, 'Jerry Walker', 'Elizabeth Clark', 'other', 'Big usually that gro', 'Commercial mean heavy eye still several.', 298, 'Glass evening example only at practice.', 'Simply usually husband rule. College option since attention poor piece like. Claim discussion very vote indeed ask.', 'Left serve morning concern my nature.', 'Improve so rock sea anyone understand.', 2, 561, 'Financial necessary energy sport end.');
INSERT INTO `ems_job_post_file` (`file_id`, `job_post_id`, `application_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `uploaded_by_user_id`, `download_count`, `thumbnail_location`) VALUES (5, 1, 1, 'Patty Ramirez', 'Kayla Erickson', 'spreadsheet', 'Mrs magazine range.', 'Easy walk wrong against around.', 523, 'Gun system guy movement.', 'Tough fast hit agency ready easy surface. Few together sense per. Decide field work field.
Well apply dark happen grow free. Shoulder me at box.', 'Memory energy kind face member reveal.', 'Up situation worker.', 1, 745, 'Indicate how interview.');

-- ems_community_file (5 records)
INSERT INTO `ems_community_file` (`file_id`, `community_id`, `post_id`, `event_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `uploaded_by_user_id`, `download_count`, `thumbnail_location`) VALUES (1, 1, 2, 2, 'Willie Butler', 'Mr. Peter Dixon', 'presentation', 'Claim western cover.', 'Admit not arrive.', 96, 'Time explain artist art.', 'Nor media man present sound never film. Reason west determine expert. Radio throw view wall.
Democrat doctor child wonder science around. We white successful subject.', 'Medical probably what if science economy.', 'As than leg cultural where.', 1, 147, NULL);
INSERT INTO `ems_community_file` (`file_id`, `community_id`, `post_id`, `event_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `uploaded_by_user_id`, `download_count`, `thumbnail_location`) VALUES (2, 2, 1, 1, 'Christian Ray', 'Lisa Burke', 'html', 'Perform build forget', 'Wall government agreement rock if.', 435, 'Point ball rule training probably light.', 'Throughout finish themselves family anyone provide institution. Than despite general base movie human behavior act. Standard ball pass miss back information.', 'Reason room note most toward.', NULL, 2, 925, 'Probably admit start.');
INSERT INTO `ems_community_file` (`file_id`, `community_id`, `post_id`, `event_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `uploaded_by_user_id`, `download_count`, `thumbnail_location`) VALUES (3, 2, 2, 1, 'Michelle Jordan', 'Jennifer Conley', 'html', 'Really difficult bab', 'Fear serious body Congress none.', 726, 'Structure drug sister.', 'Discover least wind so newspaper someone difficult. Mouth present much player rise.
Program area election baby bag paper long step. Fight character happy. Weight drive should tax.', 'Bag form put buy decide partner.', 'Generation accept speak clearly career customer.', 2, 892, 'Writer make amount expect.');
INSERT INTO `ems_community_file` (`file_id`, `community_id`, `post_id`, `event_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `uploaded_by_user_id`, `download_count`, `thumbnail_location`) VALUES (4, 1, 2, 2, 'Steven Chambers', 'Lauren Phillips', 'html', 'Plan itself country ', 'Whole rich show if trade institution.', 503, 'Cut especially stop current everything.', 'Front even expect provide west. Individual become establish party pull manager.
Above instead end receive wall than.
Evidence spend suggest music outside board. Send you attack group new recent.', 'Writer doctor skill plant.', 'Hundred interesting apply.', 1, 293, 'These energy create personal its tough.');
INSERT INTO `ems_community_file` (`file_id`, `community_id`, `post_id`, `event_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `uploaded_by_user_id`, `download_count`, `thumbnail_location`) VALUES (5, 1, 2, 2, 'Parker Osborne', 'Nicole Jacobs', 'spreadsheet', 'Care claim nation fo', 'Mention vote evidence.', 44, 'Blood such back ok.', 'Teacher nation modern doctor. Design debate yes agent true.
Where paper growth.', 'Shake exist arm keep side.', NULL, 2, 666, 'Gun change I.');

-- ems_market_trend_file (5 records)
INSERT INTO `ems_market_trend_file` (`file_id`, `trend_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `source`, `report_date`, `download_count`, `thumbnail_location`) VALUES (1, 2, 'Patricia Potts', 'Lori Powers', 'image', 'Throw four bring fee', 'They mission foreign hot popular finally.', 103, 'Early safe somebody real yes.', 'Over camera sometimes boy. Cold speech camera Congress.', 'Development admit any still.', 'Talk from realize.', 'Letter view management local maybe.', '2023-06-11', 753, NULL);
INSERT INTO `ems_market_trend_file` (`file_id`, `trend_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `source`, `report_date`, `download_count`, `thumbnail_location`) VALUES (2, 2, 'Joshua Carter', 'Keith Vang', 'html', 'Control many imagine', 'Above bit debate significant.', 923, 'Heavy husband ten three federal.', 'Couple spend value send hope. Up prevent since top. Animal high stay politics box.', 'Collection mother no camera.', 'Begin skill respond.', 'Court protect have past support.', '2022-11-22', NULL, 'Pretty enjoy million young worker reason.');
INSERT INTO `ems_market_trend_file` (`file_id`, `trend_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `source`, `report_date`, `download_count`, `thumbnail_location`) VALUES (3, 1, 'Louis Kim', 'Sheri Myers', 'markdown', 'Daughter edge will f', 'Employee indicate mother.', 544, 'School miss firm why agent.', 'Exactly town sing hotel person. Account follow way away air while. Message act everybody both traditional her success.', 'Sister management store.', 'Throw argue side Congress social whether.', 'Specific democratic property chance price their.', '2023-05-08', 648, 'Also standard main medical.');
INSERT INTO `ems_market_trend_file` (`file_id`, `trend_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `source`, `report_date`, `download_count`, `thumbnail_location`) VALUES (4, 2, 'Carlos Reed', 'Amy Hall', 'audio', 'Figure month dark.', 'Believe prevent field fear happy.', 565, 'Still collection full.', 'Member grow last why.
Line high nice social throw it. Me civil early alone evening.
Grow subject even Democrat financial who. Per push another as wish tax. Scene personal me past stop reason small.', 'Under amount population young.', 'Soon administration end.', 'Argue be short.', NULL, NULL, 'Paper low blue.');
INSERT INTO `ems_market_trend_file` (`file_id`, `trend_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `source`, `report_date`, `download_count`, `thumbnail_location`) VALUES (5, 2, 'Karen Lane', 'Leslie Beasley', 'audio', 'Reveal focus directo', 'Plan Republican out conference necessary.', 601, 'Record such pick according thousand.', 'Positive around class cost. Begin computer degree mention college air strong.
Plan natural generation project. Finish school apply. Case upon wide short.', 'Others building new why difficult.', 'Challenge happen western.', NULL, '2021-07-26', 539, 'But example far.');

-- system_config (5 records)
INSERT INTO `system_config` (`config_key`, `config_value`, `created_at`, `updated_at`) VALUES ('Eight research century color item protect.', 'Per event especially business production current.', '2024-12-14T06:44:07', '2026-01-11T17:10:48');
INSERT INTO `system_config` (`config_key`, `config_value`, `created_at`, `updated_at`) VALUES ('Race security purpose when eight.', 'Sell rise product kitchen.', '2026-01-27T01:30:20', '2026-01-27T14:12:55');
INSERT INTO `system_config` (`config_key`, `config_value`, `created_at`, `updated_at`) VALUES ('Dog science bar foot factor.', 'Probably run character.', '2024-11-25T11:59:04', '2025-07-06T11:54:52');
INSERT INTO `system_config` (`config_key`, `config_value`, `created_at`, `updated_at`) VALUES ('Item prepare it word trouble pretty.', 'Note often great mind board begin.', '2025-08-28T08:03:29', '2025-06-12T02:19:26');
INSERT INTO `system_config` (`config_key`, `config_value`, `created_at`, `updated_at`) VALUES ('Or whole project form teacher.', 'Town better main rather remain.', '2024-07-25T16:31:46', '2025-01-22T23:59:26');

-- auth_user (2 records)
INSERT INTO `auth_user` (`auth_user_id`, `username`, `email`, `password_hash`, `is_active`, `is_super_user`, `created_at`, `updated_at`) VALUES (1, 'stephentaylor', 'mark13@example.com', '$2b$12$V3U1Xq3ChNa7PK3woe23P.bdhsNApqg8wNsI6pC9TJ13fDG4IS29e', 1, 1, '2024-05-06T05:49:26', '2024-03-26T11:33:29');
INSERT INTO `auth_user` (`auth_user_id`, `username`, `email`, `password_hash`, `is_active`, `is_super_user`, `created_at`, `updated_at`) VALUES (2, 'twise', 'williamsdouglas@example.net', '$2b$12$PXhyQ1ns1gi3Wynv31wfPOwcN8YJYOtx/OamP4U.kXsc0vWCcPgna', 1, 1, '2025-12-08T12:32:08', '2024-08-23T15:35:04');

-- user_group (2 records)
INSERT INTO `user_group` (`group_id`, `group_name`, `description`, `is_super_group`, `created_at`, `created_by_auth_user_id`) VALUES (1, 'Brandon White', 'Attention recognize either really magazine. Structure today woman meet.
Talk claim age available cold seat also serve. My what send letter.', 1, '2025-08-17T22:09:16', 2);
INSERT INTO `user_group` (`group_id`, `group_name`, `description`, `is_super_group`, `created_at`, `created_by_auth_user_id`) VALUES (2, 'Phillip Pena', 'Of choose firm. Movement face gas east. At truth feel too use month.
Notice large later next market speech eat. Myself sense him me size.', 1, '2025-01-04T02:45:58', 2);

-- user_group_membership (5 records)
INSERT INTO `user_group_membership` (`membership_id`, `auth_user_id`, `group_id`, `granted_at`, `granted_by_auth_user_id`, `expires_at`) VALUES (1, 1, 2, NULL, 1, '2025-09-16T22:45:38');
INSERT INTO `user_group_membership` (`membership_id`, `auth_user_id`, `group_id`, `granted_at`, `granted_by_auth_user_id`, `expires_at`) VALUES (2, 2, 2, '2025-10-24T13:53:13', 2, '2024-08-21T05:44:27');
INSERT INTO `user_group_membership` (`membership_id`, `auth_user_id`, `group_id`, `granted_at`, `granted_by_auth_user_id`, `expires_at`) VALUES (3, 1, 1, '2025-06-07T00:04:25', 2, '2025-09-01T13:42:44');
INSERT INTO `user_group_membership` (`membership_id`, `auth_user_id`, `group_id`, `granted_at`, `granted_by_auth_user_id`, `expires_at`) VALUES (4, 1, 1, NULL, 1, '2025-05-19T05:38:10');
INSERT INTO `user_group_membership` (`membership_id`, `auth_user_id`, `group_id`, `granted_at`, `granted_by_auth_user_id`, `expires_at`) VALUES (5, 2, 1, '2024-07-19T07:51:06', 1, '2025-11-28T00:48:24');

-- document_group_type (2 records)
INSERT INTO `document_group_type` (`type_id`, `type_name`, `description`) VALUES (1, 'Steven Peterson', 'Majority foot indeed door herself base quality main.
Pay process mean easy defense ground back. Within debate find degree local call. Else seven not other miss art source.');
INSERT INTO `document_group_type` (`type_id`, `type_name`, `description`) VALUES (2, 'Jill Wright', 'Game old beautiful feeling. Simple long growth knowledge citizen three seat. Be tax get great him place.
Cause physical oil bad if white international stage. Hear current window station green.');

-- document_group (2 records)
INSERT INTO `document_group` (`document_group_id`, `group_name`, `description`, `group_type_id`, `created_at`, `created_by_auth_user_id`) VALUES (1, 'Anthony Walter', 'Two fire base seek ability. Child argue city rather let.
Task institution hundred west. Water order investment. Center sister break already commercial become drive.', 1, '2024-12-16T19:55:51', 2);
INSERT INTO `document_group` (`document_group_id`, `group_name`, `description`, `group_type_id`, `created_at`, `created_by_auth_user_id`) VALUES (2, 'Morgan Moss', 'Something ask skin. Knowledge national ever around matter eye town. Tend production indicate skill cell person.', 2, '2025-03-06T00:01:16', 2);

-- document_group_table_scope (5 records)
INSERT INTO `document_group_table_scope` (`scope_id`, `document_group_id`, `table_name`, `access_level`, `allow_read`, `allow_create`, `allow_update`, `allow_delete`, `allow_grant_access`, `allow_export`, `allow_share`, `allow_audit`, `created_at`) VALUES (1, 1, 'Colleen Walters', 'ADMIN', 0, 0, 1, 0, 1, 0, 1, 1, '2025-01-29T00:14:13');
INSERT INTO `document_group_table_scope` (`scope_id`, `document_group_id`, `table_name`, `access_level`, `allow_read`, `allow_create`, `allow_update`, `allow_delete`, `allow_grant_access`, `allow_export`, `allow_share`, `allow_audit`, `created_at`) VALUES (2, 1, 'Edward Davis', 'USER', NULL, 0, 0, 1, 1, 1, 1, 0, '2025-10-30T18:45:50');
INSERT INTO `document_group_table_scope` (`scope_id`, `document_group_id`, `table_name`, `access_level`, `allow_read`, `allow_create`, `allow_update`, `allow_delete`, `allow_grant_access`, `allow_export`, `allow_share`, `allow_audit`, `created_at`) VALUES (3, 1, 'Carlos Moore', 'ADMIN', 0, 1, 0, 0, 0, 1, 1, 0, '2024-11-08T16:58:12');
INSERT INTO `document_group_table_scope` (`scope_id`, `document_group_id`, `table_name`, `access_level`, `allow_read`, `allow_create`, `allow_update`, `allow_delete`, `allow_grant_access`, `allow_export`, `allow_share`, `allow_audit`, `created_at`) VALUES (4, 1, 'Steven Rubio', 'ADMIN', 0, 1, 0, 0, NULL, 1, 0, 1, '2025-06-24T23:23:33');
INSERT INTO `document_group_table_scope` (`scope_id`, `document_group_id`, `table_name`, `access_level`, `allow_read`, `allow_create`, `allow_update`, `allow_delete`, `allow_grant_access`, `allow_export`, `allow_share`, `allow_audit`, `created_at`) VALUES (5, 1, 'Mr. Justin Brown', 'USER', 1, 0, 1, 1, 0, 1, 0, 0, '2025-06-26T11:56:55');

-- document_group_table_record_scope (5 records)
INSERT INTO `document_group_table_record_scope` (`record_scope_id`, `document_group_id`, `table_name`, `record_id`, `allow_read`, `allow_create`, `allow_update`, `allow_delete`, `allow_grant_access`, `allow_export`, `allow_share`, `allow_audit`, `created_at`) VALUES (1, 2, 'Mark Hill', 108, 1, 0, 1, 0, 1, 0, 1, 0, '2025-11-28T08:48:31');
INSERT INTO `document_group_table_record_scope` (`record_scope_id`, `document_group_id`, `table_name`, `record_id`, `allow_read`, `allow_create`, `allow_update`, `allow_delete`, `allow_grant_access`, `allow_export`, `allow_share`, `allow_audit`, `created_at`) VALUES (2, 1, 'Robert Johnson', 364, 0, 0, 0, NULL, 0, 1, NULL, 0, '2026-02-09T00:05:16');
INSERT INTO `document_group_table_record_scope` (`record_scope_id`, `document_group_id`, `table_name`, `record_id`, `allow_read`, `allow_create`, `allow_update`, `allow_delete`, `allow_grant_access`, `allow_export`, `allow_share`, `allow_audit`, `created_at`) VALUES (3, 1, 'Victoria Price', 618, 1, 0, 1, 1, 1, 1, 1, 0, '2025-01-23T19:26:51');
INSERT INTO `document_group_table_record_scope` (`record_scope_id`, `document_group_id`, `table_name`, `record_id`, `allow_read`, `allow_create`, `allow_update`, `allow_delete`, `allow_grant_access`, `allow_export`, `allow_share`, `allow_audit`, `created_at`) VALUES (4, 2, 'James Ryan', 709, 1, 1, 0, 0, 1, 0, 1, 1, '2024-05-09T20:56:30');
INSERT INTO `document_group_table_record_scope` (`record_scope_id`, `document_group_id`, `table_name`, `record_id`, `allow_read`, `allow_create`, `allow_update`, `allow_delete`, `allow_grant_access`, `allow_export`, `allow_share`, `allow_audit`, `created_at`) VALUES (5, 2, 'Bryan Davis', 342, 1, 1, 0, 0, 0, 1, 1, 0, '2024-04-20T15:12:26');

-- document_group_query_scope (2 records)
INSERT INTO `document_group_query_scope` (`query_scope_id`, `document_group_id`, `query_name`, `scope_mode`, `created_at`) VALUES (1, 1, 'Mary Smith', 'SPECIFIC_RECORDS', '2025-11-24T14:42:04');
INSERT INTO `document_group_query_scope` (`query_scope_id`, `document_group_id`, `query_name`, `scope_mode`, `created_at`) VALUES (2, 1, 'Mary Cook', 'ALL_MATCHING', '2026-01-01T13:45:07');

-- document_group_query_record_scope (5 records)
INSERT INTO `document_group_query_record_scope` (`query_record_scope_id`, `query_scope_id`, `table_name`, `record_id`, `created_at`) VALUES (1, 1, 'Donna Saunders', 901, '2025-01-26T06:37:53');
INSERT INTO `document_group_query_record_scope` (`query_record_scope_id`, `query_scope_id`, `table_name`, `record_id`, `created_at`) VALUES (2, 1, 'Kevin Short', 808, NULL);
INSERT INTO `document_group_query_record_scope` (`query_record_scope_id`, `query_scope_id`, `table_name`, `record_id`, `created_at`) VALUES (3, 1, 'Melody Harris', 437, '2024-12-10T15:20:22');
INSERT INTO `document_group_query_record_scope` (`query_record_scope_id`, `query_scope_id`, `table_name`, `record_id`, `created_at`) VALUES (4, 1, 'Donna Martinez', 435, '2025-03-05T13:48:54');
INSERT INTO `document_group_query_record_scope` (`query_record_scope_id`, `query_scope_id`, `table_name`, `record_id`, `created_at`) VALUES (5, 1, 'Daniel Kaiser', 616, '2024-09-11T02:28:13');

-- document_group_membership (5 records)
INSERT INTO `document_group_membership` (`membership_id`, `document_group_id`, `auth_user_id`, `user_group_id`, `granted_at`, `granted_by_auth_user_id`, `expires_at`) VALUES (1, 2, 2, 1, '2024-12-16T21:58:29', 2, '2024-04-25T10:09:01');
INSERT INTO `document_group_membership` (`membership_id`, `document_group_id`, `auth_user_id`, `user_group_id`, `granted_at`, `granted_by_auth_user_id`, `expires_at`) VALUES (2, 1, 1, 1, '2025-08-18T05:31:08', 2, '2024-09-06T23:26:48');
INSERT INTO `document_group_membership` (`membership_id`, `document_group_id`, `auth_user_id`, `user_group_id`, `granted_at`, `granted_by_auth_user_id`, `expires_at`) VALUES (3, 2, 2, 1, '2026-01-23T09:57:06', 1, '2025-06-02T15:35:39');
INSERT INTO `document_group_membership` (`membership_id`, `document_group_id`, `auth_user_id`, `user_group_id`, `granted_at`, `granted_by_auth_user_id`, `expires_at`) VALUES (4, 1, 2, 1, '2025-12-05T06:14:19', 1, '2026-02-24T00:16:49');
INSERT INTO `document_group_membership` (`membership_id`, `document_group_id`, `auth_user_id`, `user_group_id`, `granted_at`, `granted_by_auth_user_id`, `expires_at`) VALUES (5, 2, 1, 1, '2025-11-05T18:57:12', 1, '2025-09-26T16:02:33');

-- access_audit_log (5 records)
INSERT INTO `access_audit_log` (`audit_id`, `auth_user_id`, `action`, `table_name`, `record_id`, `access_granted`, `denial_reason`, `ip_address`, `user_agent`, `accessed_at`) VALUES (1, 2, 'Beyond put director still.', 'Daniel Fuller', 938, 0, 'Weight pressure well.', '907 Jackson Plaza Apt. 373, West Jacqueline, ', 'Energy eat onto.', '2025-02-09T17:37:41');
INSERT INTO `access_audit_log` (`audit_id`, `auth_user_id`, `action`, `table_name`, `record_id`, `access_granted`, `denial_reason`, `ip_address`, `user_agent`, `accessed_at`) VALUES (2, 1, 'Week drop technology too front media.', 'Matthew Lewis', 329, 0, 'Hand miss western interview.', '307 Tina Plaza Apt. 080, Carrollport, GU 4776', 'Section hear class owner.', '2024-05-14T05:22:47');
INSERT INTO `access_audit_log` (`audit_id`, `auth_user_id`, `action`, `table_name`, `record_id`, `access_granted`, `denial_reason`, `ip_address`, `user_agent`, `accessed_at`) VALUES (3, 1, 'Collection hear reduce sport ball reach stuff.', 'Trevor Miller', 772, 0, 'Mr expect six trip wrong subject.', 'PSC 2165, Box 4153, APO AE 11842', 'Interesting feeling property stuff carry.', '2024-10-13T05:19:55');
INSERT INTO `access_audit_log` (`audit_id`, `auth_user_id`, `action`, `table_name`, `record_id`, `access_granted`, `denial_reason`, `ip_address`, `user_agent`, `accessed_at`) VALUES (4, 1, 'Claim network I.', 'Kimberly Edwards', 464, 1, 'Do since process music war.', '862 Moyer Island, Cameronton, IA 97331', 'Thus record member job environmental.', '2025-09-14T14:28:34');
INSERT INTO `access_audit_log` (`audit_id`, `auth_user_id`, `action`, `table_name`, `record_id`, `access_granted`, `denial_reason`, `ip_address`, `user_agent`, `accessed_at`) VALUES (5, 2, 'Government real figure.', 'Ashley Nguyen', 84, 0, 'Player bad next claim address.', '231 Michelle Park Apt. 258, Port Dawn, WA 602', 'Kid agent race economic.', '2024-05-20T14:25:38');

-- super_user_action_log (5 records)
INSERT INTO `super_user_action_log` (`action_log_id`, `auth_user_id`, `action`, `target_table`, `target_record_id`, `justification`, `performed_at`) VALUES (1, 1, 'Remember almost about financial party true.', 'Former identify street.', 896, 'Ground sing lawyer among civil example.', '2025-01-19T12:21:41');
INSERT INTO `super_user_action_log` (`action_log_id`, `auth_user_id`, `action`, `target_table`, `target_record_id`, `justification`, `performed_at`) VALUES (2, 2, 'Play actually true.', 'Rather morning shoulder produce sing.', 981, 'Help later information student.', '2025-01-22T04:30:14');
INSERT INTO `super_user_action_log` (`action_log_id`, `auth_user_id`, `action`, `target_table`, `target_record_id`, `justification`, `performed_at`) VALUES (3, 1, 'Stuff hard listen strong.', 'Player investment issue seat tough.', 326, 'Exactly natural none century.', '2025-06-20T00:30:27');
INSERT INTO `super_user_action_log` (`action_log_id`, `auth_user_id`, `action`, `target_table`, `target_record_id`, `justification`, `performed_at`) VALUES (4, 2, 'Once relationship senior pretty maintain.', 'Around he team forward billion change.', 713, 'Everything skill heavy white.', '2025-07-13T21:34:57');
INSERT INTO `super_user_action_log` (`action_log_id`, `auth_user_id`, `action`, `target_table`, `target_record_id`, `justification`, `performed_at`) VALUES (5, 2, 'Unit standard day entire.', 'Administration ago sometimes.', 915, 'Space Congress tell throw drop goal.', NULL);

-- oauth2_provider (2 records)
INSERT INTO `oauth2_provider` (`provider_id`, `provider_name`, `display_name`, `client_id`, `client_secret`, `authorization_uri`, `token_uri`, `user_info_uri`, `jwk_set_uri`, `issuer_uri`, `scope`, `is_enabled`, `created_at`, `updated_at`) VALUES (1, 'Mr. Alexander Jones', 'Darryl Berry', 'To necessary thank vote big.', 'Major discover player parent.', 'Light individual degree.', NULL, 'Follow half we network inside product.', 'Throw indeed analysis dog I bad.', 'Process easy training.', 'These them professional.', 0, '2024-07-19T04:55:56', '2024-11-22T00:54:05');
INSERT INTO `oauth2_provider` (`provider_id`, `provider_name`, `display_name`, `client_id`, `client_secret`, `authorization_uri`, `token_uri`, `user_info_uri`, `jwk_set_uri`, `issuer_uri`, `scope`, `is_enabled`, `created_at`, `updated_at`) VALUES (2, 'Leon Johnson', 'Brian Conley', 'Marriage spend evening suggest.', 'Different stock address man star.', 'Time think two still yard.', NULL, 'Agent employee debate player.', NULL, 'Save television put Congress this friend.', 'Call thank serious most listen plan.', 1, '2025-03-29T00:21:53', '2025-05-09T06:19:24');

-- oauth2_linked_account (5 records)
INSERT INTO `oauth2_linked_account` (`linked_account_id`, `auth_user_id`, `provider_id`, `provider_user_id`, `provider_username`, `provider_email`, `access_token`, `refresh_token`, `token_expires_at`, `linked_at`, `last_login_at`) VALUES (1, 1, 2, 'Into land make last war.', 'johnsonvalerie', NULL, NULL, 'Short brother establish.', '2026-02-25T01:16:04', '2025-03-13T01:44:47', '2024-05-01T22:32:52');
INSERT INTO `oauth2_linked_account` (`linked_account_id`, `auth_user_id`, `provider_id`, `provider_user_id`, `provider_username`, `provider_email`, `access_token`, `refresh_token`, `token_expires_at`, `linked_at`, `last_login_at`) VALUES (2, 1, 2, 'Protect watch page.', 'robert75', 'owise@example.org', NULL, 'Month tax attention.', '2024-10-07T07:52:27', '2025-05-24T02:02:40', '2025-10-31T11:52:31');
INSERT INTO `oauth2_linked_account` (`linked_account_id`, `auth_user_id`, `provider_id`, `provider_user_id`, `provider_username`, `provider_email`, `access_token`, `refresh_token`, `token_expires_at`, `linked_at`, `last_login_at`) VALUES (3, 1, 1, 'Between begin risk art.', 'gregory11', NULL, 'Officer field seven born research.', 'Evidence arm race.', NULL, '2024-08-20T06:54:08', '2026-02-26T21:21:10');
INSERT INTO `oauth2_linked_account` (`linked_account_id`, `auth_user_id`, `provider_id`, `provider_user_id`, `provider_username`, `provider_email`, `access_token`, `refresh_token`, `token_expires_at`, `linked_at`, `last_login_at`) VALUES (4, 1, 2, 'From media they cause Republican.', 'johnsonemily', 'traceyday@example.org', 'Yes energy condition sign game drive shake.', 'Their key necessary blue choose.', '2025-05-18T07:36:03', '2025-10-20T12:20:12', '2026-01-22T22:49:16');
INSERT INTO `oauth2_linked_account` (`linked_account_id`, `auth_user_id`, `provider_id`, `provider_user_id`, `provider_username`, `provider_email`, `access_token`, `refresh_token`, `token_expires_at`, `linked_at`, `last_login_at`) VALUES (5, 1, 1, 'Environmental food respond.', 'johngonzalez', 'vanessaneal@example.net', 'Set artist approach.', 'Current too above might space.', '2024-07-26T00:02:42', '2025-01-18T04:45:54', '2025-10-19T15:09:23');

SET FOREIGN_KEY_CHECKS = 1;
