-- Generated test data
-- Generated at: 2026-03-30T15:44:30.122417
-- Total records: 456

SET FOREIGN_KEY_CHECKS = 0;

-- ems_user (2 records)
INSERT INTO `ems_user` (`user_id`, `first_name`, `last_name`, `gender`, `date_of_birth`, `email_address`, `user_name`, `encrypted_password`, `phone_number`, `profile_photo`, `is_active`, `is_entity`) VALUES (1, 'Kathryn', 'Robinson', 'other', '2025-03-12', 'qwilkinson@example.org', 'ooconnor', 'c(cw1OgZ9H', '001-409-809-6147x849', 'Population Democrat election draw dream hold.', 0, 1);
INSERT INTO `ems_user` (`user_id`, `first_name`, `last_name`, `gender`, `date_of_birth`, `email_address`, `user_name`, `encrypted_password`, `phone_number`, `profile_photo`, `is_active`, `is_entity`) VALUES (2, 'Cory', 'Munoz', 'female', '2022-06-29', 'nhopkins@example.org', 'robertskelly', 'Zs7PbgrR^@', '001-433-987-1880', 'Story fall shake onto.', 1, 0);

-- ems_user_property_group (2 records)
INSERT INTO `ems_user_property_group` (`group_id`, `group_name`, `group_description`, `user_id`, `is_active`) VALUES (1, 'Madeline Watkins', 'American safe per around. Available dog not bad.
Realize about maintain try least police within leader. Require network system hold forward though.', 2, 1);
INSERT INTO `ems_user_property_group` (`group_id`, `group_name`, `group_description`, `user_id`, `is_active`) VALUES (2, 'David Graham', 'Yard follow black agency. Step six option.
Mrs impact day fact. Discover suggest perform campaign say we radio.
Indicate one center candidate else study stop. Activity agree three near unit federal.', 2, NULL);

-- ems_user_property (2 records)
INSERT INTO `ems_user_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `user_id`) VALUES (1, 'Keith Reyes', 'Toward after pretty somebody under statement.', 'Myself again care reality.', NULL, 2, 2);
INSERT INTO `ems_user_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `user_id`) VALUES (2, 'Gary Mack', 'Purpose area force later outside sound.', 'Energy per officer.', 'Its church top. Inside whatever entire reveal future. Name woman to create remain moment why car.
Admit than the would finish collection. Same indeed law me cut street none.', 1, 1);

-- ems_institution (2 records)
INSERT INTO `ems_institution` (`institution_id`, `name`, `description`, `moto`, `institution_type_id`, `website`, `contact_email`, `contact_phone`, `is_active`, `is_entity`) VALUES (1, 'Robert Berry DDS', 'Feel cell sport must for start. Carry better professional.
Many amount special spring question feeling matter. Environmental fire behavior within.', 'Station industry four.', 35, NULL, 'petersonmelissa@example.org', NULL, 0, 0);
INSERT INTO `ems_institution` (`institution_id`, `name`, `description`, `moto`, `institution_type_id`, `website`, `contact_email`, `contact_phone`, `is_active`, `is_entity`) VALUES (2, 'Joshua Butler', NULL, 'Shoulder than western way front.', 433, NULL, 'lauren10@example.com', '272.587.5945', 1, 0);

-- ems_institution_property_group (2 records)
INSERT INTO `ems_institution_property_group` (`group_id`, `group_name`, `group_description`, `institution_id`, `is_active`) VALUES (1, 'Steven Todd', 'Sign man require order. Business capital street.
Speak feel free.
Travel how nation pass foreign increase increase live.
Pressure rate note action bar. Into similar point.', 1, 1);
INSERT INTO `ems_institution_property_group` (`group_id`, `group_name`, `group_description`, `institution_id`, `is_active`) VALUES (2, 'Julie Sims', 'Civil sell impact hope them especially. Major claim again laugh happen resource.
Wife federal easy run off discussion thank method. Win laugh people but leg wide.', 2, 0);

-- ems_institution_property (2 records)
INSERT INTO `ems_institution_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `institution_id`) VALUES (1, 'Lindsey Adams', 'Green simply west professional project.', 'Where wide media.', 'Film any wear suddenly friend. Free person sing laugh situation evening sister.
Sense mission low building man. Worker throughout case left modern.', 2, 2);
INSERT INTO `ems_institution_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `institution_id`) VALUES (2, 'Laura Larson', 'Whatever miss meeting.', 'Necessary house inside.', NULL, 1, 2);

-- ems_candidate_institute_link (5 records)
INSERT INTO `ems_candidate_institute_link` (`link_id`, `user_id`, `institution_id`, `comment`, `status`) VALUES (1, 1, 1, 'Music baby behind small drop.', 'Like community ahead decade scene store.');
INSERT INTO `ems_candidate_institute_link` (`link_id`, `user_id`, `institution_id`, `comment`, `status`) VALUES (2, 1, 2, 'Bed such since about.', 'Major customer a myself.');
INSERT INTO `ems_candidate_institute_link` (`link_id`, `user_id`, `institution_id`, `comment`, `status`) VALUES (3, 1, 1, 'Economic yard hotel on.', NULL);
INSERT INTO `ems_candidate_institute_link` (`link_id`, `user_id`, `institution_id`, `comment`, `status`) VALUES (4, 2, 1, 'Imagine difference final chair method section.', 'Network scientist particular happy foot.');
INSERT INTO `ems_candidate_institute_link` (`link_id`, `user_id`, `institution_id`, `comment`, `status`) VALUES (5, 1, 2, 'Happy own nearly use.', 'Fear nor another real herself camera.');

-- ems_user_institute_property_link (5 records)
INSERT INTO `ems_user_institute_property_link` (`link_id`, `user_id`, `property_id`, `comment`) VALUES (1, 1, 2, NULL);
INSERT INTO `ems_user_institute_property_link` (`link_id`, `user_id`, `property_id`, `comment`) VALUES (2, 1, 2, 'Approach reveal major writer price new.');
INSERT INTO `ems_user_institute_property_link` (`link_id`, `user_id`, `property_id`, `comment`) VALUES (3, 2, 2, 'Week positive trial much.');
INSERT INTO `ems_user_institute_property_link` (`link_id`, `user_id`, `property_id`, `comment`) VALUES (4, 2, 1, 'Not lot mean tax measure.');
INSERT INTO `ems_user_institute_property_link` (`link_id`, `user_id`, `property_id`, `comment`) VALUES (5, 2, 2, 'Program on might.');

-- ems_course (2 records)
INSERT INTO `ems_course` (`course_id`, `course_name`, `description`, `outcomes`, `course_type_id`, `is_published`, `price`, `duration_weeks`, `institution_id`, `is_entity`) VALUES (1, 'Christopher Cummings', 'Recently Congress early fly bank white. Who land member this sound morning wide.
Itself market view fill. Another if add condition fall save marriage.', 'Glass air five foot eight.', 101, 0, 92010964.61, 598, 1, 1);
INSERT INTO `ems_course` (`course_id`, `course_name`, `description`, `outcomes`, `course_type_id`, `is_published`, `price`, `duration_weeks`, `institution_id`, `is_entity`) VALUES (2, 'Dana Jordan', 'Standard mention sit that close. Hand most few address. North high imagine third food daughter total.
Room energy show girl response organization subject.', 'Protect loss four.', 751, NULL, 45559214.88, 245, 2, 1);

-- ems_course_property_group (2 records)
INSERT INTO `ems_course_property_group` (`group_id`, `group_name`, `group_description`, `course_id`, `is_active`) VALUES (1, 'Christopher Robinson', NULL, 1, 0);
INSERT INTO `ems_course_property_group` (`group_id`, `group_name`, `group_description`, `course_id`, `is_active`) VALUES (2, 'Jasmine Manning', 'Purpose seven face admit impact job drive eye. Whole bank along only.
Until citizen billion half according. That face season forward anything big.', 1, NULL);

-- ems_course_property (5 records)
INSERT INTO `ems_course_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `course_id`) VALUES (1, 'Rebecca Herrera', NULL, 'Prepare wait long.', 'Price election author everyone. Show successful main then beyond. Window role single main international close.', 2, 2);
INSERT INTO `ems_course_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `course_id`) VALUES (2, 'Sheila Meyer', 'Including stay strategy sister exist adult.', 'Mind majority movement return cover.', 'Market occur break officer necessary service.
Floor everything camera customer example. Thank rate eat single.', 1, 2);
INSERT INTO `ems_course_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `course_id`) VALUES (3, 'Kathryn Benitez', 'Center according each must identify.', 'Such daughter behavior.', 'General Republican reality threat toward. Personal defense size end.', 1, 2);
INSERT INTO `ems_course_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `course_id`) VALUES (4, 'Tyler Schmidt', 'Couple lot million discussion consider at.', 'Throw number away product.', 'Likely although development rock. Up serious artist so discuss level this continue.
Bit yet either nation. Task so option. Whole under sing conference clear war.', 1, 1);
INSERT INTO `ems_course_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `course_id`) VALUES (5, 'Bradley Greene', 'Far bank main black left model.', 'Everyone develop total week.', 'Hold network live any factor plant to.
Party exist at officer even name. Anyone everyone wait partner hospital party. Expect back before medical rich join politics.', 1, 2);

-- ems_user_course_link (5 records)
INSERT INTO `ems_user_course_link` (`link_id`, `user_id`, `course_id`, `role`) VALUES (1, 1, 1, 'Represent bill system.');
INSERT INTO `ems_user_course_link` (`link_id`, `user_id`, `course_id`, `role`) VALUES (2, 2, 1, 'Investment drop generation resource.');
INSERT INTO `ems_user_course_link` (`link_id`, `user_id`, `course_id`, `role`) VALUES (3, 2, 1, 'Six open method.');
INSERT INTO `ems_user_course_link` (`link_id`, `user_id`, `course_id`, `role`) VALUES (4, 2, 1, 'Say life very sell.');
INSERT INTO `ems_user_course_link` (`link_id`, `user_id`, `course_id`, `role`) VALUES (5, 2, 2, 'Let degree as end low radio.');

-- ems_user_course_wishlist (5 records)
INSERT INTO `ems_user_course_wishlist` (`wish_id`, `user_id`, `course_id`, `comment`) VALUES (1, 2, 2, 'Stand property resource.');
INSERT INTO `ems_user_course_wishlist` (`wish_id`, `user_id`, `course_id`, `comment`) VALUES (2, 2, 2, 'Management rule question.');
INSERT INTO `ems_user_course_wishlist` (`wish_id`, `user_id`, `course_id`, `comment`) VALUES (3, 2, 2, 'Green try reflect garden wall should.');
INSERT INTO `ems_user_course_wishlist` (`wish_id`, `user_id`, `course_id`, `comment`) VALUES (4, 2, 2, 'Stuff help bag.');
INSERT INTO `ems_user_course_wishlist` (`wish_id`, `user_id`, `course_id`, `comment`) VALUES (5, 1, 1, NULL);

-- ems_user_course_purchase (5 records)
INSERT INTO `ems_user_course_purchase` (`purchase_id`, `user_id`, `course_id`, `comment`, `amount`, `transaction_id`, `purchased_on`) VALUES (1, 2, 2, 'Step increase left most state.', 50743205.35, 'Provide name hand for father all.', '2024-08-18T15:29:43');
INSERT INTO `ems_user_course_purchase` (`purchase_id`, `user_id`, `course_id`, `comment`, `amount`, `transaction_id`, `purchased_on`) VALUES (2, 1, 2, 'Start hope body ready.', 32299761.85, 'Star western international probably.', '2025-06-14T12:41:43');
INSERT INTO `ems_user_course_purchase` (`purchase_id`, `user_id`, `course_id`, `comment`, `amount`, `transaction_id`, `purchased_on`) VALUES (3, 2, 2, 'Control fish assume.', 77960567.59, 'Specific whatever share minute agree national.', '2026-01-15T19:45:38');
INSERT INTO `ems_user_course_purchase` (`purchase_id`, `user_id`, `course_id`, `comment`, `amount`, `transaction_id`, `purchased_on`) VALUES (4, 2, 1, 'Oil behavior apply break recognize your.', 71243165.84, 'As raise agency star.', '2025-02-13T08:34:03');
INSERT INTO `ems_user_course_purchase` (`purchase_id`, `user_id`, `course_id`, `comment`, `amount`, `transaction_id`, `purchased_on`) VALUES (5, 2, 1, 'Garden human never statement perform.', 9916736.49, NULL, '2024-05-29T14:23:58');

-- ems_job_post (2 records)
INSERT INTO `ems_job_post` (`job_post_id`, `job_post_subject`, `job_post_description`, `institution_id`, `location`, `salary_range`, `posted_on`, `expires_on`, `is_active`, `is_entity`) VALUES (1, 'Happen really respond.', 'Heavy heart answer business. Positive born step daughter certainly determine heavy. Beautiful in statement easy star if ten.', 2, 'Any pressure who house line open.', 'Per often politics field.', '2025-06-27T22:49:00', '2024-11-10T07:26:18', 1, 0);
INSERT INTO `ems_job_post` (`job_post_id`, `job_post_subject`, `job_post_description`, `institution_id`, `location`, `salary_range`, `posted_on`, `expires_on`, `is_active`, `is_entity`) VALUES (2, 'Either body reason camera current.', 'Identify check environmental best better seat enough. On federal seek all suddenly.
Budget where religious here. Material response according general condition send.', 2, 'Agreement cup age point meet ask.', 'Four no radio half rise.', '2025-10-13T23:23:07', '2026-03-21T14:45:59', NULL, 1);

-- ems_job_post_property_group (2 records)
INSERT INTO `ems_job_post_property_group` (`group_id`, `group_name`, `group_description`, `job_post_id`) VALUES (1, 'Amber Ward', 'Back difficult game our man station. This parent federal artist.', 2);
INSERT INTO `ems_job_post_property_group` (`group_id`, `group_name`, `group_description`, `job_post_id`) VALUES (2, 'Jamie Moody', 'Interesting force service admit eye arm herself. American none street rise decade benefit. Set special give senior person land. Risk source middle yes else explain until.', 1);

-- ems_job_post_property (5 records)
INSERT INTO `ems_job_post_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `job_post_id`) VALUES (1, 'Shannon Copeland', 'Who education huge smile fine technology.', 'Eight from key explain second within.', 'Current degree north might act. Or magazine minute stand until record.
Paper far PM ability. Focus investment step TV try.
Mrs drug mind alone sure woman crime. Road there beat candidate.', 1, 2);
INSERT INTO `ems_job_post_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `job_post_id`) VALUES (2, 'Mr. Anthony Lane', 'System same what authority exactly change.', 'Head risk similar quite.', 'Discover hard name moment book area memory.
Week small left sell huge low catch measure. Attack dream ten least participant race. Safe agreement property sort body.', 1, 1);
INSERT INTO `ems_job_post_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `job_post_id`) VALUES (3, 'Travis Woodard', 'Science likely story door method.', 'Attention similar there produce computer property.', 'Plan move relationship watch. Miss PM TV although so court thank.
Bag occur debate experience. Computer social back discuss probably difficult sometimes. Your these break at.', 2, 2);
INSERT INTO `ems_job_post_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `job_post_id`) VALUES (4, 'Amy Cardenas', 'Loss tax still woman tonight.', 'Point kind bad black may.', NULL, 2, 2);
INSERT INTO `ems_job_post_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `job_post_id`) VALUES (5, 'Jason Graham', 'Allow gas church able affect.', 'Among collection maintain worry hundred.', 'Become fire brother in play necessary. Entire threat chair save recently change. Green lead local sure customer. Role listen establish treat admit finally.', 1, 2);

-- ems_user_job_post_bookmark (5 records)
INSERT INTO `ems_user_job_post_bookmark` (`bookmark_id`, `user_id`, `job_post_id`, `comment`) VALUES (1, 1, 2, 'Both practice sea decade.');
INSERT INTO `ems_user_job_post_bookmark` (`bookmark_id`, `user_id`, `job_post_id`, `comment`) VALUES (2, 2, 1, 'Upon old guess notice.');
INSERT INTO `ems_user_job_post_bookmark` (`bookmark_id`, `user_id`, `job_post_id`, `comment`) VALUES (3, 2, 2, 'Step today special.');
INSERT INTO `ems_user_job_post_bookmark` (`bookmark_id`, `user_id`, `job_post_id`, `comment`) VALUES (4, 2, 1, 'Plan a bit peace.');
INSERT INTO `ems_user_job_post_bookmark` (`bookmark_id`, `user_id`, `job_post_id`, `comment`) VALUES (5, 1, 1, 'Letter his five lot letter.');

-- ems_job_post_user_bookmark (5 records)
INSERT INTO `ems_job_post_user_bookmark` (`bookmark_id`, `job_post_id`, `user_id`, `comment`) VALUES (1, 2, 2, 'Art raise impact blue similar.');
INSERT INTO `ems_job_post_user_bookmark` (`bookmark_id`, `job_post_id`, `user_id`, `comment`) VALUES (2, 2, 1, 'Long onto today lose.');
INSERT INTO `ems_job_post_user_bookmark` (`bookmark_id`, `job_post_id`, `user_id`, `comment`) VALUES (3, 1, 1, 'Which rest personal into conference.');
INSERT INTO `ems_job_post_user_bookmark` (`bookmark_id`, `job_post_id`, `user_id`, `comment`) VALUES (4, 2, 1, 'You certainly man.');
INSERT INTO `ems_job_post_user_bookmark` (`bookmark_id`, `job_post_id`, `user_id`, `comment`) VALUES (5, 2, 1, 'Author again throw picture recent.');

-- ems_subscription_payment_history (5 records)
INSERT INTO `ems_subscription_payment_history` (`payment_id`, `user_id`, `amount`, `subscription_type`, `transaction_details`, `transaction_reference`, `payment_on`) VALUES (1, 2, 4964146286.69, 'Throughout safe section author never.', '{}', 'Father fund our.', '2024-06-16T08:37:09');
INSERT INTO `ems_subscription_payment_history` (`payment_id`, `user_id`, `amount`, `subscription_type`, `transaction_details`, `transaction_reference`, `payment_on`) VALUES (2, 2, 3488459926.55, 'Change south thing which build team.', '{}', 'Water necessary military.', NULL);
INSERT INTO `ems_subscription_payment_history` (`payment_id`, `user_id`, `amount`, `subscription_type`, `transaction_details`, `transaction_reference`, `payment_on`) VALUES (3, 1, 2063311297.46, 'Smile well town difference.', '{}', 'North north walk cut.', '2024-04-13T14:55:32');
INSERT INTO `ems_subscription_payment_history` (`payment_id`, `user_id`, `amount`, `subscription_type`, `transaction_details`, `transaction_reference`, `payment_on`) VALUES (4, 2, 1848532725.82, 'Lead continue blood very.', '{}', 'Task paper former thing run kind.', NULL);
INSERT INTO `ems_subscription_payment_history` (`payment_id`, `user_id`, `amount`, `subscription_type`, `transaction_details`, `transaction_reference`, `payment_on`) VALUES (5, 1, 6890791750.24, 'Ever prove pretty produce thousand street.', NULL, 'Their start product activity.', '2024-04-12T12:48:43');

-- ems_community (2 records)
INSERT INTO `ems_community` (`community_id`, `institute_id`, `name`, `description`, `group_owner_user_id`, `is_entity`) VALUES (1, 1, 'Connie Hubbard', 'Occur task door decide sense. Just now apply area production group myself mother. Wall seven expect will system at.', 2, 0);
INSERT INTO `ems_community` (`community_id`, `institute_id`, `name`, `description`, `group_owner_user_id`, `is_entity`) VALUES (2, 2, 'David Hopkins', 'Simply discover represent rest particularly. Indicate out he make fish certainly.', 2, 0);

-- ems_community_property_group (2 records)
INSERT INTO `ems_community_property_group` (`group_id`, `group_name`, `group_description`, `community_id`) VALUES (1, 'Jessica Shah', 'Notice training free. Important bring grow spend west play.
There pass appear generation late thing how. Likely home run partner person.', 2);
INSERT INTO `ems_community_property_group` (`group_id`, `group_name`, `group_description`, `community_id`) VALUES (2, 'Susan Hernandez MD', 'Kid while each set. Child none high parent relationship particularly the. Girl center couple research.
Senior suddenly control admit sing other his. Chance conference current.', 2);

-- ems_community_property (2 records)
INSERT INTO `ems_community_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `community_id`) VALUES (1, 'Jennifer Mcmahon', 'As state book.', 'Government court ahead may value human.', 'Already fight son color. Old loss quality carry wide arrive. Four sing whatever avoid result boy station. Road first suddenly about.', 1, 1);
INSERT INTO `ems_community_property` (`property_id`, `property_name`, `property_value`, `property_type`, `property_description`, `group_id`, `community_id`) VALUES (2, 'Shannon Lucas', 'Ball office tough statement camera small.', 'Statement agency camera woman.', 'Body speech however run others respond. Thus local note baby.
Pass piece heavy several hair. Training much despite throughout put hope. Safe before future.', 1, 1);

-- ems_community_user_link (5 records)
INSERT INTO `ems_community_user_link` (`link_id`, `community_id`, `user_id`, `role`, `comment`) VALUES (1, 1, 2, 'Interview probably toward rate morning special.', 'Opportunity program important music.');
INSERT INTO `ems_community_user_link` (`link_id`, `community_id`, `user_id`, `role`, `comment`) VALUES (2, 2, 1, 'Cause vote fast conference force.', 'Throughout such part beat one course.');
INSERT INTO `ems_community_user_link` (`link_id`, `community_id`, `user_id`, `role`, `comment`) VALUES (3, 2, 1, NULL, NULL);
INSERT INTO `ems_community_user_link` (`link_id`, `community_id`, `user_id`, `role`, `comment`) VALUES (4, 1, 1, 'Example least and media forget product hair.', 'Southern single without despite house body.');
INSERT INTO `ems_community_user_link` (`link_id`, `community_id`, `user_id`, `role`, `comment`) VALUES (5, 2, 1, 'Foot citizen chance body.', 'Total accept individual wait black.');

-- ems_community_property_user_link (5 records)
INSERT INTO `ems_community_property_user_link` (`link_id`, `community_property_id`, `user_id`, `comment`) VALUES (1, 1, 2, 'Guy seem break media toward.');
INSERT INTO `ems_community_property_user_link` (`link_id`, `community_property_id`, `user_id`, `comment`) VALUES (2, 2, 1, 'Happen build government radio plan near.');
INSERT INTO `ems_community_property_user_link` (`link_id`, `community_property_id`, `user_id`, `comment`) VALUES (3, 1, 1, 'Show improve field together tend.');
INSERT INTO `ems_community_property_user_link` (`link_id`, `community_property_id`, `user_id`, `comment`) VALUES (4, 2, 1, 'Up scene try agent paper.');
INSERT INTO `ems_community_property_user_link` (`link_id`, `community_property_id`, `user_id`, `comment`) VALUES (5, 2, 1, 'Face maintain traditional.');

-- ems_community_user_post (2 records)
INSERT INTO `ems_community_user_post` (`post_id`, `community_id`, `user_id`, `post`, `is_pinned`) VALUES (1, 1, 1, '{}', 0);
INSERT INTO `ems_community_user_post` (`post_id`, `community_id`, `user_id`, `post`, `is_pinned`) VALUES (2, 1, 1, '{}', 1);

-- ems_community_post_link (5 records)
INSERT INTO `ems_community_post_link` (`link_id`, `post_id`, `community_id`) VALUES (1, 2, 1);
INSERT INTO `ems_community_post_link` (`link_id`, `post_id`, `community_id`) VALUES (2, 2, 2);
INSERT INTO `ems_community_post_link` (`link_id`, `post_id`, `community_id`) VALUES (3, 2, 1);
INSERT INTO `ems_community_post_link` (`link_id`, `post_id`, `community_id`) VALUES (4, 1, 2);
INSERT INTO `ems_community_post_link` (`link_id`, `post_id`, `community_id`) VALUES (5, 1, 1);

-- ems_post_emogi (2 records)
INSERT INTO `ems_post_emogi` (`emogi_id`, `name`, `description`, `file_location`) VALUES (1, 'Kimberly Cook', 'Manager way money parent toward well. Bar resource service election care. She process front us lawyer.', 'Many gun among bank seat third.');
INSERT INTO `ems_post_emogi` (`emogi_id`, `name`, `description`, `file_location`) VALUES (2, 'Brittany May', 'Front more or early peace owner learn. Travel decide reduce want really understand house.
Realize recent call your actually scene. Page say speak. Several sit kitchen without several way instead.', 'According describe again meet.');

-- ems_emogi_post_user_link (5 records)
INSERT INTO `ems_emogi_post_user_link` (`link_id`, `emogi_id`, `post_id`, `user_id`) VALUES (1, 2, 1, 2);
INSERT INTO `ems_emogi_post_user_link` (`link_id`, `emogi_id`, `post_id`, `user_id`) VALUES (2, 1, 1, 2);
INSERT INTO `ems_emogi_post_user_link` (`link_id`, `emogi_id`, `post_id`, `user_id`) VALUES (3, 2, 2, 1);
INSERT INTO `ems_emogi_post_user_link` (`link_id`, `emogi_id`, `post_id`, `user_id`) VALUES (4, 1, 2, 1);
INSERT INTO `ems_emogi_post_user_link` (`link_id`, `emogi_id`, `post_id`, `user_id`) VALUES (5, 1, 1, 1);

-- ems_post_flag (5 records)
INSERT INTO `ems_post_flag` (`flag_id`, `type`, `user_id`, `post_id`, `reason`, `flagged_on`) VALUES (1, 'Win foot wish.', 1, 2, 'Identify answer he true alone side.', '2026-01-01T18:27:45');
INSERT INTO `ems_post_flag` (`flag_id`, `type`, `user_id`, `post_id`, `reason`, `flagged_on`) VALUES (2, 'Just admit action any.', 2, 2, 'Expert pick soon memory relate investment.', '2025-09-12T06:37:09');
INSERT INTO `ems_post_flag` (`flag_id`, `type`, `user_id`, `post_id`, `reason`, `flagged_on`) VALUES (3, 'Decide note strong short.', 2, 2, 'Always send next.', '2025-02-17T15:07:35');
INSERT INTO `ems_post_flag` (`flag_id`, `type`, `user_id`, `post_id`, `reason`, `flagged_on`) VALUES (4, 'Together job along stay billion write.', 2, 1, 'Concern read will.', '2024-07-23T19:09:49');
INSERT INTO `ems_post_flag` (`flag_id`, `type`, `user_id`, `post_id`, `reason`, `flagged_on`) VALUES (5, 'Mention particular party.', 1, 2, 'Young they player health reality learn.', '2025-03-14T14:06:45');

-- ems_post_comment (2 records)
INSERT INTO `ems_post_comment` (`comment_id`, `post_id`, `comment`, `user_id`) VALUES (1, 2, 'He professional management.', 1);
INSERT INTO `ems_post_comment` (`comment_id`, `post_id`, `comment`, `user_id`) VALUES (2, 1, 'Daughter west series event thank eat.', 2);

-- ems_post_comment_emogi_link (5 records)
INSERT INTO `ems_post_comment_emogi_link` (`link_id`, `comment_id`, `emogi_id`, `user_id`) VALUES (1, 1, 1, 2);
INSERT INTO `ems_post_comment_emogi_link` (`link_id`, `comment_id`, `emogi_id`, `user_id`) VALUES (2, 2, 1, 1);
INSERT INTO `ems_post_comment_emogi_link` (`link_id`, `comment_id`, `emogi_id`, `user_id`) VALUES (3, 1, 2, 2);
INSERT INTO `ems_post_comment_emogi_link` (`link_id`, `comment_id`, `emogi_id`, `user_id`) VALUES (4, 1, 1, 1);
INSERT INTO `ems_post_comment_emogi_link` (`link_id`, `comment_id`, `emogi_id`, `user_id`) VALUES (5, 1, 1, 2);

-- ems_ai_user_profile_evaluation_parameter_group (2 records)
INSERT INTO `ems_ai_user_profile_evaluation_parameter_group` (`group_id`, `group_name`, `description`) VALUES (1, 'Cathy Miller', 'Wall peace than much degree else ground. Consider benefit national theory morning poor debate.
Add close school wonder tell PM.
Walk program another social blue TV science camera.');
INSERT INTO `ems_ai_user_profile_evaluation_parameter_group` (`group_id`, `group_name`, `description`) VALUES (2, 'Maria Hale', 'Program catch story last skill. Happen mission simple. Hour best manager identify take. Marriage fish wall health exist fight.
White picture our none relate. Expert community hand fund.');

-- ems_ai_user_profile_evaluation_parameter (5 records)
INSERT INTO `ems_ai_user_profile_evaluation_parameter` (`parameter_id`, `parameter_name`, `group_id`, `parameter_value`) VALUES (1, 'Leah Boyd DDS', 1, '{}');
INSERT INTO `ems_ai_user_profile_evaluation_parameter` (`parameter_id`, `parameter_name`, `group_id`, `parameter_value`) VALUES (2, 'Jennifer Sanchez', 1, '{}');
INSERT INTO `ems_ai_user_profile_evaluation_parameter` (`parameter_id`, `parameter_name`, `group_id`, `parameter_value`) VALUES (3, 'Joseph Simpson', 1, '{}');
INSERT INTO `ems_ai_user_profile_evaluation_parameter` (`parameter_id`, `parameter_name`, `group_id`, `parameter_value`) VALUES (4, 'Jessica Dixon', 2, NULL);
INSERT INTO `ems_ai_user_profile_evaluation_parameter` (`parameter_id`, `parameter_name`, `group_id`, `parameter_value`) VALUES (5, 'Robert Ward', 2, '{}');

-- ems_ai_user_profile_evaluation (5 records)
INSERT INTO `ems_ai_user_profile_evaluation` (`evaluation_id`, `user_id`, `property_id`, `evaluation_summary`, `rating`) VALUES (1, 1, 1, '{}', 3.73);
INSERT INTO `ems_ai_user_profile_evaluation` (`evaluation_id`, `user_id`, `property_id`, `evaluation_summary`, `rating`) VALUES (2, 2, 2, '{}', 3.77);
INSERT INTO `ems_ai_user_profile_evaluation` (`evaluation_id`, `user_id`, `property_id`, `evaluation_summary`, `rating`) VALUES (3, 1, 2, '{}', 1.69);
INSERT INTO `ems_ai_user_profile_evaluation` (`evaluation_id`, `user_id`, `property_id`, `evaluation_summary`, `rating`) VALUES (4, 1, 1, '{}', 2.63);
INSERT INTO `ems_ai_user_profile_evaluation` (`evaluation_id`, `user_id`, `property_id`, `evaluation_summary`, `rating`) VALUES (5, 2, 1, '{}', 2.03);

-- ems_ai_evaluation_parameter_group (2 records)
INSERT INTO `ems_ai_evaluation_parameter_group` (`group_id`, `group_name`, `description`) VALUES (1, 'Matthew Hurley', 'Whole purpose develop science light certain late. Either top father old guess feel a. Science visit art.');
INSERT INTO `ems_ai_evaluation_parameter_group` (`group_id`, `group_name`, `description`) VALUES (2, 'Jay Washington', 'But site Mrs total record. Doctor possible act among contain truth. Or site today.');

-- ems_ai_evaluation_parameter (5 records)
INSERT INTO `ems_ai_evaluation_parameter` (`parameter_id`, `parameter_name`, `parameter_group_id`, `parameter_value`) VALUES (1, 'Mr. Michael Turner', 1, NULL);
INSERT INTO `ems_ai_evaluation_parameter` (`parameter_id`, `parameter_name`, `parameter_group_id`, `parameter_value`) VALUES (2, 'Erik Smith', 2, '{}');
INSERT INTO `ems_ai_evaluation_parameter` (`parameter_id`, `parameter_name`, `parameter_group_id`, `parameter_value`) VALUES (3, 'Christine Gonzales', 2, '{}');
INSERT INTO `ems_ai_evaluation_parameter` (`parameter_id`, `parameter_name`, `parameter_group_id`, `parameter_value`) VALUES (4, 'Debra King', 2, NULL);
INSERT INTO `ems_ai_evaluation_parameter` (`parameter_id`, `parameter_name`, `parameter_group_id`, `parameter_value`) VALUES (5, 'Tyler Davis', 2, '{}');

-- ems_ai_institution_profile_evaluation (5 records)
INSERT INTO `ems_ai_institution_profile_evaluation` (`evaluation_id`, `institution_id`, `evaluation_summary`, `rating`) VALUES (1, 2, '{}', 3.81);
INSERT INTO `ems_ai_institution_profile_evaluation` (`evaluation_id`, `institution_id`, `evaluation_summary`, `rating`) VALUES (2, 1, '{}', 2.06);
INSERT INTO `ems_ai_institution_profile_evaluation` (`evaluation_id`, `institution_id`, `evaluation_summary`, `rating`) VALUES (3, 1, '{}', 1.52);
INSERT INTO `ems_ai_institution_profile_evaluation` (`evaluation_id`, `institution_id`, `evaluation_summary`, `rating`) VALUES (4, 1, '{}', 3.4);
INSERT INTO `ems_ai_institution_profile_evaluation` (`evaluation_id`, `institution_id`, `evaluation_summary`, `rating`) VALUES (5, 2, '{}', 3.02);

-- ems_ai_job_recommendation (5 records)
INSERT INTO `ems_ai_job_recommendation` (`preference_id`, `job_post_id`, `profile_id`, `preference_rating`, `recommendation_summary`) VALUES (1, 1, 402, 1.8, '{}');
INSERT INTO `ems_ai_job_recommendation` (`preference_id`, `job_post_id`, `profile_id`, `preference_rating`, `recommendation_summary`) VALUES (2, 2, 890, 4.56, NULL);
INSERT INTO `ems_ai_job_recommendation` (`preference_id`, `job_post_id`, `profile_id`, `preference_rating`, `recommendation_summary`) VALUES (3, 2, 955, 1.95, '{}');
INSERT INTO `ems_ai_job_recommendation` (`preference_id`, `job_post_id`, `profile_id`, `preference_rating`, `recommendation_summary`) VALUES (4, 2, 973, 2.5, '{}');
INSERT INTO `ems_ai_job_recommendation` (`preference_id`, `job_post_id`, `profile_id`, `preference_rating`, `recommendation_summary`) VALUES (5, 1, 188, 2.01, '{}');

-- ems_ai_community_post_evaluation (5 records)
INSERT INTO `ems_ai_community_post_evaluation` (`evaluation_id`, `post_id`, `evaluation_summary`, `rating`) VALUES (1, 1, '{}', 3.34);
INSERT INTO `ems_ai_community_post_evaluation` (`evaluation_id`, `post_id`, `evaluation_summary`, `rating`) VALUES (2, 2, '{}', 3.97);
INSERT INTO `ems_ai_community_post_evaluation` (`evaluation_id`, `post_id`, `evaluation_summary`, `rating`) VALUES (3, 2, NULL, 2.94);
INSERT INTO `ems_ai_community_post_evaluation` (`evaluation_id`, `post_id`, `evaluation_summary`, `rating`) VALUES (4, 1, '{}', NULL);
INSERT INTO `ems_ai_community_post_evaluation` (`evaluation_id`, `post_id`, `evaluation_summary`, `rating`) VALUES (5, 2, '{}', NULL);

-- ems_ai_market_trend_parameter_group (2 records)
INSERT INTO `ems_ai_market_trend_parameter_group` (`group_id`, `group_name`, `description`, `trend_id`) VALUES (1, 'Steven Powers', NULL, 171);
INSERT INTO `ems_ai_market_trend_parameter_group` (`group_id`, `group_name`, `description`, `trend_id`) VALUES (2, 'Jennifer Mendoza', 'Like history morning politics often news. Away race treat must new happy.
Big travel east third because. Nearly send blood decade become director.
Image sometimes new marriage. Job so word not vote.', 939);

-- ems_ai_market_trend_parameter (5 records)
INSERT INTO `ems_ai_market_trend_parameter` (`parameter_id`, `parameter_name`, `parameter_value`, `group_id`) VALUES (1, 'Pamela Baker', '{}', 2);
INSERT INTO `ems_ai_market_trend_parameter` (`parameter_id`, `parameter_name`, `parameter_value`, `group_id`) VALUES (2, 'Noah Hahn', '{}', 2);
INSERT INTO `ems_ai_market_trend_parameter` (`parameter_id`, `parameter_name`, `parameter_value`, `group_id`) VALUES (3, 'Laura Davis', '{}', 1);
INSERT INTO `ems_ai_market_trend_parameter` (`parameter_id`, `parameter_name`, `parameter_value`, `group_id`) VALUES (4, 'Michelle Clayton', '{}', 1);
INSERT INTO `ems_ai_market_trend_parameter` (`parameter_id`, `parameter_name`, `parameter_value`, `group_id`) VALUES (5, 'Kendra Rollins', '{}', 1);

-- ems_ai_market_trend_property (2 records)
INSERT INTO `ems_ai_market_trend_property` (`trend_id`, `trend_name`, `trend_description`) VALUES (1, 'Courtney Russo', 'Institution piece per coach surface health marriage eye. Budget require she mother baby final teacher above.');
INSERT INTO `ems_ai_market_trend_property` (`trend_id`, `trend_name`, `trend_description`) VALUES (2, 'Scott Gross', 'Child carry continue very lead economic. By property nation.
Current two message whole during instead. Development owner adult rather beautiful once bank fall. Mr ok walk agency.');

-- ems_user_profile_document (5 records)
INSERT INTO `ems_user_profile_document` (`document_id`, `user_id`, `title`, `document`, `document_type`) VALUES (1, 1, NULL, '{}', 'Indicate cause not street.');
INSERT INTO `ems_user_profile_document` (`document_id`, `user_id`, `title`, `document`, `document_type`) VALUES (2, 2, 'Study piece accept six environmental this there', '{}', NULL);
INSERT INTO `ems_user_profile_document` (`document_id`, `user_id`, `title`, `document`, `document_type`) VALUES (3, 2, 'War group expect system sing next', '{}', 'Be argue former.');
INSERT INTO `ems_user_profile_document` (`document_id`, `user_id`, `title`, `document`, `document_type`) VALUES (4, 2, 'Though determine nor account mouth', '{}', NULL);
INSERT INTO `ems_user_profile_document` (`document_id`, `user_id`, `title`, `document`, `document_type`) VALUES (5, 1, 'Third husband agree friend finish', '{}', 'Put drop actually forward small money.');

-- ems_institution_profile_document (5 records)
INSERT INTO `ems_institution_profile_document` (`document_id`, `institution_id`, `title`, `document`, `document_type`) VALUES (1, 1, 'None research hair coach', '{}', 'Wonder war green themselves should hair nature.');
INSERT INTO `ems_institution_profile_document` (`document_id`, `institution_id`, `title`, `document`, `document_type`) VALUES (2, 1, 'Strong chair natural who', '{}', 'Away perhaps cut him it.');
INSERT INTO `ems_institution_profile_document` (`document_id`, `institution_id`, `title`, `document`, `document_type`) VALUES (3, 2, 'Wonder him day sport do bed', '{}', 'Probably on effort raise.');
INSERT INTO `ems_institution_profile_document` (`document_id`, `institution_id`, `title`, `document`, `document_type`) VALUES (4, 1, 'Especially money Democrat', '{}', NULL);
INSERT INTO `ems_institution_profile_document` (`document_id`, `institution_id`, `title`, `document`, `document_type`) VALUES (5, 1, 'Develop strategy computer pretty shoulder truth raise', '{}', NULL);

-- ems_course_document_group (2 records)
INSERT INTO `ems_course_document_group` (`group_id`, `group_name`, `group_description`, `course_id`, `is_active`) VALUES (1, 'Ashley Hampton', 'Left across attention. Prove fire early focus one. Focus country once rich.
Close dinner trial prevent off. Able poor staff age now family.', 2, 1);
INSERT INTO `ems_course_document_group` (`group_id`, `group_name`, `group_description`, `course_id`, `is_active`) VALUES (2, 'Dawn Lambert', 'Follow whether together reason others possible early we. Pass something candidate life. Mouth wish politics network win form born.', 1, 0);

-- ems_course_document (5 records)
INSERT INTO `ems_course_document` (`document_id`, `course_id`, `group_id`, `title`, `document`, `document_type`, `file_name`) VALUES (1, 2, 2, 'Second arrive political anyone must before word gas', '{}', 'Consider heart human answer responsibility.', 'Tracy Moses');
INSERT INTO `ems_course_document` (`document_id`, `course_id`, `group_id`, `title`, `document`, `document_type`, `file_name`) VALUES (2, 2, 1, 'Anything about response Mr she could', '{}', NULL, 'George Clarke');
INSERT INTO `ems_course_document` (`document_id`, `course_id`, `group_id`, `title`, `document`, `document_type`, `file_name`) VALUES (3, 2, 2, 'We economic mind operation factor', '{}', 'Hit also behavior enough.', 'Danielle Lopez');
INSERT INTO `ems_course_document` (`document_id`, `course_id`, `group_id`, `title`, `document`, `document_type`, `file_name`) VALUES (4, 2, 1, 'Detail item late explain', '{}', 'Ten again else already.', 'Christopher Harris');
INSERT INTO `ems_course_document` (`document_id`, `course_id`, `group_id`, `title`, `document`, `document_type`, `file_name`) VALUES (5, 1, 1, 'Guess drop language authority', '{}', 'Throw again career fill free.', 'Garrett Kelly');

-- ems_market_trend_document (5 records)
INSERT INTO `ems_market_trend_document` (`document_id`, `trend_id`, `title`, `document`, `document_type`) VALUES (1, 2, 'Opportunity message ready', '{}', 'Guess beautiful another.');
INSERT INTO `ems_market_trend_document` (`document_id`, `trend_id`, `title`, `document`, `document_type`) VALUES (2, 2, 'Professional trip draw above capital term man', '{}', 'Method cover area middle.');
INSERT INTO `ems_market_trend_document` (`document_id`, `trend_id`, `title`, `document`, `document_type`) VALUES (3, 1, 'Back available among perhaps', '{}', 'Opportunity system technology edge.');
INSERT INTO `ems_market_trend_document` (`document_id`, `trend_id`, `title`, `document`, `document_type`) VALUES (4, 1, 'East poor report mouth listen necessary', '{}', 'Staff give dark.');
INSERT INTO `ems_market_trend_document` (`document_id`, `trend_id`, `title`, `document`, `document_type`) VALUES (5, 2, 'Among prepare too best crime military', '{}', 'Behavior bed through seat.');

-- ems_job_post_document (5 records)
INSERT INTO `ems_job_post_document` (`document_id`, `job_post_id`, `title`, `document`, `document_type`, `file_name`) VALUES (1, 2, NULL, '{}', 'Gas answer air apply cut my.', 'Carl Cooper');
INSERT INTO `ems_job_post_document` (`document_id`, `job_post_id`, `title`, `document`, `document_type`, `file_name`) VALUES (2, 2, 'Of present energy industry office responsibility development reveal', '{}', NULL, 'Cindy Shields');
INSERT INTO `ems_job_post_document` (`document_id`, `job_post_id`, `title`, `document`, `document_type`, `file_name`) VALUES (3, 1, 'Spring believe hair identify dog', '{}', 'Small attorney see chance ten hour.', 'Richard Schwartz');
INSERT INTO `ems_job_post_document` (`document_id`, `job_post_id`, `title`, `document`, `document_type`, `file_name`) VALUES (4, 2, 'Today admit present blue nation', '{}', 'Moment remember speak anything.', 'Cynthia Lewis');
INSERT INTO `ems_job_post_document` (`document_id`, `job_post_id`, `title`, `document`, `document_type`, `file_name`) VALUES (5, 2, 'Peace four image listen although hotel glass', '{}', 'Notice give full.', 'Pamela Blackwell');

-- ems_user_education (5 records)
INSERT INTO `ems_user_education` (`education_id`, `user_id`, `institution_id`, `degree_type`, `field_of_study`, `specialization`, `start_date`, `end_date`, `grade_gpa`, `is_verified`, `certificate_document_id`) VALUES (1, 2, 1, 'Table member either town pass federal.', 'Food realize loss.', 'Institution them agency.', '2025-12-08', '2023-05-06', 'Country great dark involve not.', 1, 588);
INSERT INTO `ems_user_education` (`education_id`, `user_id`, `institution_id`, `degree_type`, `field_of_study`, `specialization`, `start_date`, `end_date`, `grade_gpa`, `is_verified`, `certificate_document_id`) VALUES (2, 2, 1, 'Memory while low.', 'Rich run hot.', 'Upon form close three economy support.', '2021-08-02', '2023-07-12', 'Their page any resource beat.', 1, 97);
INSERT INTO `ems_user_education` (`education_id`, `user_id`, `institution_id`, `degree_type`, `field_of_study`, `specialization`, `start_date`, `end_date`, `grade_gpa`, `is_verified`, `certificate_document_id`) VALUES (3, 2, 2, 'Claim team this project hear.', 'Today yes bank.', 'Blue lawyer everyone after likely.', '2022-09-10', '2024-08-26', 'Yes mother service pattern analysis.', 1, 566);
INSERT INTO `ems_user_education` (`education_id`, `user_id`, `institution_id`, `degree_type`, `field_of_study`, `specialization`, `start_date`, `end_date`, `grade_gpa`, `is_verified`, `certificate_document_id`) VALUES (4, 2, 2, 'Edge must thought great think car.', 'Note law could himself.', 'Much peace dark traditional pull.', '2023-01-30', '2025-03-29', 'Have under bad.', 0, 178);
INSERT INTO `ems_user_education` (`education_id`, `user_id`, `institution_id`, `degree_type`, `field_of_study`, `specialization`, `start_date`, `end_date`, `grade_gpa`, `is_verified`, `certificate_document_id`) VALUES (5, 1, 1, 'Least book either then.', 'Do very loss language.', 'Five son draw.', '2021-06-22', '2023-11-21', 'Walk state site someone cold.', 0, 458);

-- ems_user_work_experience (5 records)
INSERT INTO `ems_user_work_experience` (`experience_id`, `user_id`, `institution_id`, `job_title`, `company_name`, `employment_type`, `location`, `start_date`, `end_date`, `is_current`, `responsibilities`, `achievements`, `skills_used`) VALUES (1, 2, 2, 'Off sometimes expert simple behind once', 'Luke Mcbride', 'Part-time', 'Suddenly product already spring cold traditional.', '2023-02-07', '2025-03-16', 1, 'Work course threat federal.', 'Energy rock coach high catch.', '{}');
INSERT INTO `ems_user_work_experience` (`experience_id`, `user_id`, `institution_id`, `job_title`, `company_name`, `employment_type`, `location`, `start_date`, `end_date`, `is_current`, `responsibilities`, `achievements`, `skills_used`) VALUES (2, 1, 1, 'Early woman edge raise style couple easy', 'Allison Schroeder', 'Freelance', 'At win story development same require.', '2025-11-25', '2024-11-02', NULL, 'Director I entire particularly attention stop which.', 'Answer everyone party.', '{}');
INSERT INTO `ems_user_work_experience` (`experience_id`, `user_id`, `institution_id`, `job_title`, `company_name`, `employment_type`, `location`, `start_date`, `end_date`, `is_current`, `responsibilities`, `achievements`, `skills_used`) VALUES (3, 2, 1, 'Win rock Mrs then challenge', 'Caleb Keller', NULL, 'Game mother day your.', '2026-03-25', '2025-09-07', 0, 'Baby live serious.', 'Evidence environment red create.', '{}');
INSERT INTO `ems_user_work_experience` (`experience_id`, `user_id`, `institution_id`, `job_title`, `company_name`, `employment_type`, `location`, `start_date`, `end_date`, `is_current`, `responsibilities`, `achievements`, `skills_used`) VALUES (4, 2, 1, 'Recent concern arrive finally political fall what', 'Timothy Coleman', 'Part-time', 'Particular choice student more.', '2025-10-02', NULL, 0, 'Recognize by yes project size same.', NULL, '{}');
INSERT INTO `ems_user_work_experience` (`experience_id`, `user_id`, `institution_id`, `job_title`, `company_name`, `employment_type`, `location`, `start_date`, `end_date`, `is_current`, `responsibilities`, `achievements`, `skills_used`) VALUES (5, 2, 1, 'Often leg future military price follow', 'Michelle Harris', NULL, 'Career mother make voice drug modern.', '2022-03-18', '2021-10-14', 1, 'Among picture nothing player.', 'Them around style hold.', '{}');

-- ems_user_skill (2 records)
INSERT INTO `ems_user_skill` (`skill_id`, `user_id`, `skill_name`, `skill_category`, `proficiency_level`, `years_of_experience`, `is_verified`, `verified_by_institution_id`, `endorsement_count`) VALUES (1, 2, 'David Mason', 'Region fall score seek son require.', 'Beginner', 161, 0, 2, 360);
INSERT INTO `ems_user_skill` (`skill_id`, `user_id`, `skill_name`, `skill_category`, `proficiency_level`, `years_of_experience`, `is_verified`, `verified_by_institution_id`, `endorsement_count`) VALUES (2, 2, 'David Davis', 'Require record here walk his partner.', 'Advanced', 88, 1, 1, 290);

-- ems_user_certification (5 records)
INSERT INTO `ems_user_certification` (`certification_id`, `user_id`, `certification_name`, `issuing_organization`, `institution_id`, `issue_date`, `expiry_date`, `credential_id`, `credential_url`, `certificate_document_id`, `is_verified`) VALUES (1, 2, 'Jacob Hernandez', 'Burgess and Sons', 2, '2024-09-20', '2025-10-12', 'Trial bill particularly.', 'http://www.aguilar-robinson.com/', 999, NULL);
INSERT INTO `ems_user_certification` (`certification_id`, `user_id`, `certification_name`, `issuing_organization`, `institution_id`, `issue_date`, `expiry_date`, `credential_id`, `credential_url`, `certificate_document_id`, `is_verified`) VALUES (2, 1, 'Linda Tran', 'Kim, Aguilar and Briggs', 2, '2026-03-07', '2025-10-03', 'Program happy nature.', 'https://www.whitney-gonzalez.com/', 626, 0);
INSERT INTO `ems_user_certification` (`certification_id`, `user_id`, `certification_name`, `issuing_organization`, `institution_id`, `issue_date`, `expiry_date`, `credential_id`, `credential_url`, `certificate_document_id`, `is_verified`) VALUES (3, 2, 'Carla Koch', 'Sullivan, Ali and Chavez', 2, '2021-09-04', '2024-01-04', 'Child issue spend.', 'http://www.waters.com/', 538, 0);
INSERT INTO `ems_user_certification` (`certification_id`, `user_id`, `certification_name`, `issuing_organization`, `institution_id`, `issue_date`, `expiry_date`, `credential_id`, `credential_url`, `certificate_document_id`, `is_verified`) VALUES (4, 2, 'Eduardo White', 'Anderson, Murray and Martinez', 1, '2022-09-05', NULL, 'Nor because hear wife.', 'https://www.marshall.com/', 128, 0);
INSERT INTO `ems_user_certification` (`certification_id`, `user_id`, `certification_name`, `issuing_organization`, `institution_id`, `issue_date`, `expiry_date`, `credential_id`, `credential_url`, `certificate_document_id`, `is_verified`) VALUES (5, 1, 'Peggy Craig', 'Garcia, James and Edwards', 1, '2024-02-10', '2025-01-03', 'Sing myself rock.', 'https://www.coleman.net/', 55, 1);

-- ems_user_language (5 records)
INSERT INTO `ems_user_language` (`language_id`, `user_id`, `language_name`, `proficiency_level`, `can_read`, `can_write`, `can_speak`) VALUES (1, 1, 'Brad Fowler', 'Professional', 0, 0, 0);
INSERT INTO `ems_user_language` (`language_id`, `user_id`, `language_name`, `proficiency_level`, `can_read`, `can_write`, `can_speak`) VALUES (2, 1, 'Cynthia Johnson', 'Professional', 1, 0, 0);
INSERT INTO `ems_user_language` (`language_id`, `user_id`, `language_name`, `proficiency_level`, `can_read`, `can_write`, `can_speak`) VALUES (3, 1, 'Robert Hays', 'Conversational', 0, 0, 1);
INSERT INTO `ems_user_language` (`language_id`, `user_id`, `language_name`, `proficiency_level`, `can_read`, `can_write`, `can_speak`) VALUES (4, 2, 'Danielle Hawkins', 'Native', 0, 1, 0);
INSERT INTO `ems_user_language` (`language_id`, `user_id`, `language_name`, `proficiency_level`, `can_read`, `can_write`, `can_speak`) VALUES (5, 1, 'Nicholas Ross', 'Professional', 0, 0, 1);

-- ems_user_achievement (5 records)
INSERT INTO `ems_user_achievement` (`achievement_id`, `user_id`, `title`, `description`, `achievement_type`, `issuer`, `date_achieved`, `url`, `document_id`) VALUES (1, 2, 'Room he risk voice step old hold', 'Mean prepare learn owner himself gun. Challenge family shoulder book court. Quality whether several activity.', 'Smile that player write environment.', 'Plan decade air between analysis pretty.', '2022-04-01', 'http://werner.com/', 898);
INSERT INTO `ems_user_achievement` (`achievement_id`, `user_id`, `title`, `description`, `achievement_type`, `issuer`, `date_achieved`, `url`, `document_id`) VALUES (2, 1, 'Impact TV stock six note kid real', 'Decade describe window work. Way reach pass provide this per big.
Fine hair safe three. Alone team continue serious audience yourself. Employee check lot prove.
Fish western record onto itself hand.', NULL, 'Place word base.', '2025-04-18', 'http://www.schroeder.com/', 747);
INSERT INTO `ems_user_achievement` (`achievement_id`, `user_id`, `title`, `description`, `achievement_type`, `issuer`, `date_achieved`, `url`, `document_id`) VALUES (3, 1, 'Couple trade else dream people sell', 'Produce store structure summer. Huge environment throughout reflect.
Special visit exactly hair build. Speak person future hold.', 'Safe way next financial get clearly.', 'Type range trip.', '2024-01-30', 'https://www.ashley.com/', 862);
INSERT INTO `ems_user_achievement` (`achievement_id`, `user_id`, `title`, `description`, `achievement_type`, `issuer`, `date_achieved`, `url`, `document_id`) VALUES (4, 2, 'Human strong camera', 'Method wrong young force. Defense much American relate.
Push thousand final compare end model majority memory. Single effort know.', 'Conference cover meet I cut.', 'Debate meeting figure improve.', '2023-09-25', 'https://www.russell.com/', 456);
INSERT INTO `ems_user_achievement` (`achievement_id`, `user_id`, `title`, `description`, `achievement_type`, `issuer`, `date_achieved`, `url`, `document_id`) VALUES (5, 2, 'Skin whole form others why rock popular', NULL, 'Clear community language other.', 'Pressure month personal take dream.', '2023-05-21', 'https://melton.com/', 598);

-- ems_user_social_link (5 records)
INSERT INTO `ems_user_social_link` (`link_id`, `user_id`, `platform`, `profile_url`, `is_verified`) VALUES (1, 1, 'Clear their peace.', 'http://hall.net/', 1);
INSERT INTO `ems_user_social_link` (`link_id`, `user_id`, `platform`, `profile_url`, `is_verified`) VALUES (2, 1, 'Off commercial top purpose.', 'https://cummings.info/', 0);
INSERT INTO `ems_user_social_link` (`link_id`, `user_id`, `platform`, `profile_url`, `is_verified`) VALUES (3, 1, 'Side season any financial yet.', 'http://www.jefferson-west.com/', 0);
INSERT INTO `ems_user_social_link` (`link_id`, `user_id`, `platform`, `profile_url`, `is_verified`) VALUES (4, 2, 'Education inside school commercial.', 'http://gregory.org/', 1);
INSERT INTO `ems_user_social_link` (`link_id`, `user_id`, `platform`, `profile_url`, `is_verified`) VALUES (5, 1, 'Almost fine three mind arrive.', 'http://pearson.net/', 0);

-- ems_institution_department (5 records)
INSERT INTO `ems_institution_department` (`department_id`, `institution_id`, `department_name`, `description`, `head_of_department_user_id`, `contact_email`, `contact_phone`, `is_active`) VALUES (1, 1, 'Lisa Gonzales', 'Might why understand standard. Several degree morning.
Toward pay bank up skin they. Show piece land.
Source talk beyond image citizen phone by individual. Main all maintain right.', 1, 'wellskelsey@example.net', '(927)776-9605x580', 0);
INSERT INTO `ems_institution_department` (`department_id`, `institution_id`, `department_name`, `description`, `head_of_department_user_id`, `contact_email`, `contact_phone`, `is_active`) VALUES (2, 1, 'Cody Mcneil', 'Beautiful law sort worry since life note. Network director out health avoid oil realize. Along water clear material performance summer.', 2, 'jacob02@example.com', '(577)940-7595x1135', 0);
INSERT INTO `ems_institution_department` (`department_id`, `institution_id`, `department_name`, `description`, `head_of_department_user_id`, `contact_email`, `contact_phone`, `is_active`) VALUES (3, 1, 'Haley Pierce', 'Four agreement little owner single house place. Government world simply try close firm amount somebody. Accept move vote let example own Mr. Often two close issue you.', 2, 'iperez@example.com', '+1-947-658-1089', 1);
INSERT INTO `ems_institution_department` (`department_id`, `institution_id`, `department_name`, `description`, `head_of_department_user_id`, `contact_email`, `contact_phone`, `is_active`) VALUES (4, 1, 'Jorge Hall', 'Alone issue toward behavior surface under ground. Age guess management safe blue population turn. Per lot television series action.', 1, 'mannsteven@example.com', '387.581.9767x463', NULL);
INSERT INTO `ems_institution_department` (`department_id`, `institution_id`, `department_name`, `description`, `head_of_department_user_id`, `contact_email`, `contact_phone`, `is_active`) VALUES (5, 1, 'Eric Morris', NULL, 1, 'alexis36@example.com', '730-590-5390x463', 0);

-- ems_institution_location (2 records)
INSERT INTO `ems_institution_location` (`location_id`, `institution_id`, `location_type`, `address_line1`, `address_line2`, `city`, `state_province`, `country`, `postal_code`, `latitude`, `longitude`, `is_primary`) VALUES (1, 1, 'Office', 'Fear pressure medical question alone.', 'Security join mean.', 'Brownville', 'Vermont', 'Jamaica', '28305', 90.93322228, 674.73529708, 0);
INSERT INTO `ems_institution_location` (`location_id`, `institution_id`, `location_type`, `address_line1`, `address_line2`, `city`, `state_province`, `country`, `postal_code`, `latitude`, `longitude`, `is_primary`) VALUES (2, 2, 'Office', 'Nor quickly buy each high.', 'Training above late.', 'Collinsburgh', 'Iowa', 'Equatorial Guinea', '99082', 23.63465074, 264.90762858, 0);

-- ems_institution_accreditation (5 records)
INSERT INTO `ems_institution_accreditation` (`accreditation_id`, `institution_id`, `accrediting_body`, `accreditation_type`, `accreditation_level`, `issue_date`, `expiry_date`, `certificate_document_id`, `is_active`) VALUES (1, 2, 'Easy couple top man number one.
Official summer technology wife. Idea production each second. Do possible trial mean job enough.', 'One property reveal ability.', 'Finally reduce TV blue report final.', '2021-09-02', '2023-08-06', 137, 1);
INSERT INTO `ems_institution_accreditation` (`accreditation_id`, `institution_id`, `accrediting_body`, `accreditation_type`, `accreditation_level`, `issue_date`, `expiry_date`, `certificate_document_id`, `is_active`) VALUES (2, 2, 'Stop itself and rule strategy dinner accept. Health PM force sound town add life.
Here still action fly himself next. Population him half that radio we.
Summer book them. Thousand what time person.', 'Most sort realize write voice.', 'Can white here site.', '2021-05-08', '2022-09-09', 841, 1);
INSERT INTO `ems_institution_accreditation` (`accreditation_id`, `institution_id`, `accrediting_body`, `accreditation_type`, `accreditation_level`, `issue_date`, `expiry_date`, `certificate_document_id`, `is_active`) VALUES (3, 1, 'Approach have sister hundred. World cut year western good wife possible.
Save water six decide indeed fear specific. My simply yeah billion goal majority hour.', 'Allow point word would.', 'Rise specific laugh husband including base.', '2023-12-12', '2022-11-02', 834, 1);
INSERT INTO `ems_institution_accreditation` (`accreditation_id`, `institution_id`, `accrediting_body`, `accreditation_type`, `accreditation_level`, `issue_date`, `expiry_date`, `certificate_document_id`, `is_active`) VALUES (4, 2, 'So last miss store glass kitchen. All tree newspaper receive effect nor. Mother soon light page Mr available such. Loss tax assume whether young peace morning.', 'Still plant whether industry difficult similar.', 'Most produce gun those town social.', '2023-09-17', '2023-11-20', 79, 0);
INSERT INTO `ems_institution_accreditation` (`accreditation_id`, `institution_id`, `accrediting_body`, `accreditation_type`, `accreditation_level`, `issue_date`, `expiry_date`, `certificate_document_id`, `is_active`) VALUES (5, 1, 'Anyone successful east main by small. Character father recognize nor good week.
Doctor do start trip. Trade trade yourself use sit some performance. Four price mission control section.', 'Generation charge know.', 'Democrat likely pretty carry school community.', '2023-12-04', '2023-10-19', NULL, 1);

-- ems_institution_ranking (5 records)
INSERT INTO `ems_institution_ranking` (`ranking_id`, `institution_id`, `ranking_organization`, `ranking_year`, `overall_rank`, `country_rank`, `category`, `category_rank`, `score`) VALUES (1, 1, 'Powell PLC', 22, 825, 426, 'Property some mean.', NULL, 0.55);
INSERT INTO `ems_institution_ranking` (`ranking_id`, `institution_id`, `ranking_organization`, `ranking_year`, `overall_rank`, `country_rank`, `category`, `category_rank`, `score`) VALUES (2, 2, 'Perez Group', 744, 358, 830, 'Natural strong production the.', 510, 0.74);
INSERT INTO `ems_institution_ranking` (`ranking_id`, `institution_id`, `ranking_organization`, `ranking_year`, `overall_rank`, `country_rank`, `category`, `category_rank`, `score`) VALUES (3, 1, 'Holt and Sons', 703, 485, 999, 'Thought against debate total.', 964, NULL);
INSERT INTO `ems_institution_ranking` (`ranking_id`, `institution_id`, `ranking_organization`, `ranking_year`, `overall_rank`, `country_rank`, `category`, `category_rank`, `score`) VALUES (4, 1, 'Hammond Group', 661, 909, 105, NULL, 823, 0.43);
INSERT INTO `ems_institution_ranking` (`ranking_id`, `institution_id`, `ranking_organization`, `ranking_year`, `overall_rank`, `country_rank`, `category`, `category_rank`, `score`) VALUES (5, 2, 'Phillips, Mccormick and Lloyd', 796, 433, 582, 'Interesting though stop back.', 735, 0.91);

-- ems_institution_facility (5 records)
INSERT INTO `ems_institution_facility` (`facility_id`, `institution_id`, `facility_name`, `facility_type`, `description`, `capacity`, `location_id`, `is_available`) VALUES (1, 1, 'Lindsay George', 'Pm above have chance deep.', 'Picture home star need section throw. Happy create mind election above plan.
Church thus better another any I time size.
Fire call develop strategy.', 366, 2, 1);
INSERT INTO `ems_institution_facility` (`facility_id`, `institution_id`, `facility_name`, `facility_type`, `description`, `capacity`, `location_id`, `is_available`) VALUES (2, 1, 'Sherry Green', 'South take sometimes produce scientist us.', 'Story account free debate list study. Situation role out stuff.
With area certainly husband source. Smile ball resource. Several need quite have.', 749, 1, 1);
INSERT INTO `ems_institution_facility` (`facility_id`, `institution_id`, `facility_name`, `facility_type`, `description`, `capacity`, `location_id`, `is_available`) VALUES (3, 1, 'Kyle Alexander', 'Arrive any same.', 'Responsibility sport international table likely arrive. Goal small laugh range others.
How space every develop high. Just employee law gun per. Thing from win glass will turn.', NULL, 2, 0);
INSERT INTO `ems_institution_facility` (`facility_id`, `institution_id`, `facility_name`, `facility_type`, `description`, `capacity`, `location_id`, `is_available`) VALUES (4, 1, 'Zachary Sampson', 'Through movie employee ok anyone.', 'Into operation carry how. Size could nice.
Cell not answer light partner data official. Office newspaper of old measure these.
Business size certain other room.', 561, 2, 0);
INSERT INTO `ems_institution_facility` (`facility_id`, `institution_id`, `facility_name`, `facility_type`, `description`, `capacity`, `location_id`, `is_available`) VALUES (5, 1, 'Thomas Lewis', 'Human find effect less.', 'Improve not task tell beat. Full large production stuff kind attorney.
Some all seek church performance.', 191, 2, 1);

-- ems_course_module (2 records)
INSERT INTO `ems_course_module` (`module_id`, `course_id`, `module_name`, `module_number`, `description`, `duration_hours`, `learning_objectives`, `is_mandatory`, `order_sequence`) VALUES (1, 1, 'Elizabeth Simpson', 68, NULL, 629, 'Time can responsibility customer.', 0, 110);
INSERT INTO `ems_course_module` (`module_id`, `course_id`, `module_name`, `module_number`, `description`, `duration_hours`, `learning_objectives`, `is_mandatory`, `order_sequence`) VALUES (2, 1, 'Jeremiah Reynolds', 594, NULL, 84, 'Right these audience court.', 0, 660);

-- ems_course_lesson (2 records)
INSERT INTO `ems_course_lesson` (`lesson_id`, `module_id`, `course_id`, `lesson_title`, `lesson_number`, `content_type`, `content_url`, `duration_minutes`, `is_preview_available`, `order_sequence`) VALUES (1, 1, 2, 'Region fear member first six', 765, 'Text', 'https://clark.com/', NULL, 0, 791);
INSERT INTO `ems_course_lesson` (`lesson_id`, `module_id`, `course_id`, `lesson_title`, `lesson_number`, `content_type`, `content_url`, `duration_minutes`, `is_preview_available`, `order_sequence`) VALUES (2, 2, 1, 'Forward seem deal understand list enough about', 235, 'Video', NULL, NULL, 1, 773);

-- ems_course_prerequisite (5 records)
INSERT INTO `ems_course_prerequisite` (`prerequisite_id`, `course_id`, `prerequisite_course_id`, `prerequisite_type`, `prerequisite_description`, `is_mandatory`) VALUES (1, 1, 1, 'Experience', 'Security door several unit during. Goal direction information husband PM. Through exactly provide article.
Stop today phone always. Hundred pay thus less gas thousand black.', 1);
INSERT INTO `ems_course_prerequisite` (`prerequisite_id`, `course_id`, `prerequisite_course_id`, `prerequisite_type`, `prerequisite_description`, `is_mandatory`) VALUES (2, 2, 1, 'Course', 'Senior become option add. Lawyer know consumer inside reveal again fall. Write ok activity suddenly technology.
Group today security painting worker politics. Hospital evening race star.', 0);
INSERT INTO `ems_course_prerequisite` (`prerequisite_id`, `course_id`, `prerequisite_course_id`, `prerequisite_type`, `prerequisite_description`, `is_mandatory`) VALUES (3, 2, 1, 'Skill', 'Attention he instead fast memory check start. Pick those agree sea moment trial. Decision until various.
Account wish hold two property man thousand. Become health we his.', 0);
INSERT INTO `ems_course_prerequisite` (`prerequisite_id`, `course_id`, `prerequisite_course_id`, `prerequisite_type`, `prerequisite_description`, `is_mandatory`) VALUES (4, 2, 1, 'Skill', 'Statement red moment over budget. Feeling mouth value evidence research various.
Seek dog idea away place. Police heart offer.
Admit state and head foot attorney. Official doctor less another gas.', 1);
INSERT INTO `ems_course_prerequisite` (`prerequisite_id`, `course_id`, `prerequisite_course_id`, `prerequisite_type`, `prerequisite_description`, `is_mandatory`) VALUES (5, 2, 2, 'Experience', 'Bill his policy expect fear American agreement send. Its trip though leader. List but forget deal argue amount.
Knowledge six still somebody field. Worker I while situation.', 1);

-- ems_course_instructor (5 records)
INSERT INTO `ems_course_instructor` (`instructor_link_id`, `course_id`, `user_id`, `role`, `bio`, `specialization`) VALUES (1, 2, 1, 'Guest Lecturer', NULL, 'How wife foreign draw.');
INSERT INTO `ems_course_instructor` (`instructor_link_id`, `course_id`, `user_id`, `role`, `bio`, `specialization`) VALUES (2, 2, 1, 'Teaching Assistant', 'Start about community population significant could discover. Guy street fire arrive.
And specific age article show usually. Up everybody fill sort new.', 'Ago piece police key everyone red.');
INSERT INTO `ems_course_instructor` (`instructor_link_id`, `course_id`, `user_id`, `role`, `bio`, `specialization`) VALUES (3, 1, 1, 'Lead Instructor', 'Hand American your myself here suggest. Push small up reveal. Compare campaign interesting later evening cup.
Shoulder anything wish last. Official agency morning control.', NULL);
INSERT INTO `ems_course_instructor` (`instructor_link_id`, `course_id`, `user_id`, `role`, `bio`, `specialization`) VALUES (4, 1, 1, 'Lead Instructor', 'Against thus social hit raise. Service short general scientist. Different something five.
Reflect second whole. Age show research she. Meeting sound age she news executive inside.', 'Then family present it medical.');
INSERT INTO `ems_course_instructor` (`instructor_link_id`, `course_id`, `user_id`, `role`, `bio`, `specialization`) VALUES (5, 2, 1, 'Co-Instructor', 'It by make per police hair budget ask. Early reason yeah. Democrat together along exist charge whose positive.
Let catch course program report. Character two hard yourself contain.', 'Career step land.');

-- ems_course_review (5 records)
INSERT INTO `ems_course_review` (`review_id`, `course_id`, `user_id`, `rating`, `review_title`, `review_text`, `helpful_count`, `is_verified_purchase`) VALUES (1, 1, 1, 1.5, 'Room break avoid soon guy first', 'Vote visit movie glass organization.', 421, 0);
INSERT INTO `ems_course_review` (`review_id`, `course_id`, `user_id`, `rating`, `review_title`, `review_text`, `helpful_count`, `is_verified_purchase`) VALUES (2, 1, 2, 1.6, 'Watch resource force source', 'The reach must.', 474, 0);
INSERT INTO `ems_course_review` (`review_id`, `course_id`, `user_id`, `rating`, `review_title`, `review_text`, `helpful_count`, `is_verified_purchase`) VALUES (3, 1, 2, 2.9, 'Manager stay while professional', NULL, 283, 1);
INSERT INTO `ems_course_review` (`review_id`, `course_id`, `user_id`, `rating`, `review_title`, `review_text`, `helpful_count`, `is_verified_purchase`) VALUES (4, 1, 1, 4.0, 'Sound particularly store picture style', 'Image number dinner least worker.', NULL, 0);
INSERT INTO `ems_course_review` (`review_id`, `course_id`, `user_id`, `rating`, `review_title`, `review_text`, `helpful_count`, `is_verified_purchase`) VALUES (5, 1, 1, 3.0, NULL, 'Back hour body knowledge rich TV.', 732, 1);

-- ems_course_assignment (2 records)
INSERT INTO `ems_course_assignment` (`assignment_id`, `course_id`, `module_id`, `title`, `description`, `assignment_type`, `max_score`, `passing_score`, `due_date`, `duration_minutes`, `is_mandatory`) VALUES (1, 1, 2, 'Put politics soldier', 'Author community point leave side evidence most. Over fine sometimes explain. Him point to wall end offer building.
Factor although term left. Care character information probably.', 'Exam', 321, 253, '2025-10-28T09:09:51', 54, 1);
INSERT INTO `ems_course_assignment` (`assignment_id`, `course_id`, `module_id`, `title`, `description`, `assignment_type`, `max_score`, `passing_score`, `due_date`, `duration_minutes`, `is_mandatory`) VALUES (2, 1, 1, 'Military environment authority seem rise', 'Quality everyone successful blue pay economy. Sound idea feel film. Eye attorney religious career environment employee item.', 'Project', 577, 420, '2025-08-26T16:32:27', 330, 1);

-- ems_user_course_progress (5 records)
INSERT INTO `ems_user_course_progress` (`progress_id`, `user_id`, `course_id`, `lesson_id`, `completion_percentage`, `last_accessed_at`, `time_spent_minutes`, `status`) VALUES (1, 2, 2, 2, 889.01, '2026-02-01T18:23:07', 146, 'Not Started');
INSERT INTO `ems_user_course_progress` (`progress_id`, `user_id`, `course_id`, `lesson_id`, `completion_percentage`, `last_accessed_at`, `time_spent_minutes`, `status`) VALUES (2, 1, 1, 1, 441.99, '2024-10-21T02:53:31', 551, 'Completed');
INSERT INTO `ems_user_course_progress` (`progress_id`, `user_id`, `course_id`, `lesson_id`, `completion_percentage`, `last_accessed_at`, `time_spent_minutes`, `status`) VALUES (3, 2, 1, 2, 641.18, '2024-10-28T23:57:18', 555, NULL);
INSERT INTO `ems_user_course_progress` (`progress_id`, `user_id`, `course_id`, `lesson_id`, `completion_percentage`, `last_accessed_at`, `time_spent_minutes`, `status`) VALUES (4, 1, 1, 2, 411.36, '2025-07-21T02:52:04', 848, 'Completed');
INSERT INTO `ems_user_course_progress` (`progress_id`, `user_id`, `course_id`, `lesson_id`, `completion_percentage`, `last_accessed_at`, `time_spent_minutes`, `status`) VALUES (5, 1, 1, 2, 675.63, '2024-11-11T13:59:01', 538, 'Dropped');

-- ems_user_assignment_submission (5 records)
INSERT INTO `ems_user_assignment_submission` (`submission_id`, `assignment_id`, `user_id`, `submission_content`, `submission_file_id`, `submitted_at`, `score`, `feedback`, `graded_by_user_id`, `graded_at`, `status`) VALUES (1, 1, 2, 'Why project center size. Stop leave require will state rock find.
Cause successful until life. Chance heart particularly go home.
Skin buy inside your like personal could adult. Power certain recognize control full.
List toward Mrs analysis surface item. Soon indicate foreign than school authority different.
Read myself deep. Ok moment energy shoulder reach some. Point improve total.', 556, '2025-06-14T03:59:20', 496, 'Theory meeting wrong.', 1, '2024-07-03T21:22:55', 'Resubmit Required');
INSERT INTO `ems_user_assignment_submission` (`submission_id`, `assignment_id`, `user_id`, `submission_content`, `submission_file_id`, `submitted_at`, `score`, `feedback`, `graded_by_user_id`, `graded_at`, `status`) VALUES (2, 2, 1, NULL, 628, '2024-07-24T11:37:51', 111, 'Involve world country walk.', 1, '2026-02-20T23:02:31', 'Submitted');
INSERT INTO `ems_user_assignment_submission` (`submission_id`, `assignment_id`, `user_id`, `submission_content`, `submission_file_id`, `submitted_at`, `score`, `feedback`, `graded_by_user_id`, `graded_at`, `status`) VALUES (3, 1, 1, 'Mind attorney any power ground man. Approach foot because recently who east program project. No story amount forward catch.
Social forget size movement. Method apply behavior stand piece drive. Truth course employee ready drive.
Huge attack certain control. Prove market for father certainly glass. Close miss same down than.
Section message effort set system detail hope talk. Term on fact health.
Service serious total knowledge central. Material carry lose she shoulder.', 588, '2024-08-27T21:20:16', 823, 'Parent common prepare try evidence.', 1, '2024-06-08T14:16:22', 'Resubmit Required');
INSERT INTO `ems_user_assignment_submission` (`submission_id`, `assignment_id`, `user_id`, `submission_content`, `submission_file_id`, `submitted_at`, `score`, `feedback`, `graded_by_user_id`, `graded_at`, `status`) VALUES (4, 1, 2, 'Single lead admit. Cause material somebody. Red board what. Rock really three development purpose travel chance.
Side table study service feel. Almost tough order left they collection special their. Fire thus card forward improve suffer area.
Stock suddenly recognize bank laugh create. Prove test sell probably free last west. Seven institution or president anything.
Professional small out dark wind. Above develop far threat determine indicate current crime. Quite quite low morning.', 775, NULL, 253, 'Nature science admit.', 1, NULL, 'Submitted');
INSERT INTO `ems_user_assignment_submission` (`submission_id`, `assignment_id`, `user_id`, `submission_content`, `submission_file_id`, `submitted_at`, `score`, `feedback`, `graded_by_user_id`, `graded_at`, `status`) VALUES (5, 1, 2, 'Agency listen lose apply summer season southern. Term along fear only keep Democrat.
Institution ahead sort. Young interest turn senior mention.
Participant game natural example tend feel. Leg sound those stage issue decision agree. Increase understand fire suddenly outside.
Market sit light hard treat. Worker fight unit thing model cut rate Congress.
Girl significant light executive past throughout million. Town article hear give American.', 6, '2024-11-12T18:58:19', 216, 'Find look relationship.', 1, '2025-09-26T21:50:50', 'Graded');

-- ems_job_post_requirement (5 records)
INSERT INTO `ems_job_post_requirement` (`requirement_id`, `job_post_id`, `requirement_type`, `requirement_description`, `is_mandatory`, `minimum_years`, `proficiency_level`) VALUES (1, 1, 'Certification', 'Democratic four kind doctor accept east. Record road six series fire learn. Design instead catch cup not.', 0, 205, 'Teacher sense continue.');
INSERT INTO `ems_job_post_requirement` (`requirement_id`, `job_post_id`, `requirement_type`, `requirement_description`, `is_mandatory`, `minimum_years`, `proficiency_level`) VALUES (2, 1, 'Certification', 'Democratic behavior back clearly current allow movement. Call two material sit sure kitchen security to.', 1, 849, 'Old likely quite since treat.');
INSERT INTO `ems_job_post_requirement` (`requirement_id`, `job_post_id`, `requirement_type`, `requirement_description`, `is_mandatory`, `minimum_years`, `proficiency_level`) VALUES (3, 1, 'Skill', 'Bed because claim number industry section. Yourself become important important phone.
Population here debate sea foot. Executive five hundred if nation vote trade. Some she policy account physical.', 1, 273, NULL);
INSERT INTO `ems_job_post_requirement` (`requirement_id`, `job_post_id`, `requirement_type`, `requirement_description`, `is_mandatory`, `minimum_years`, `proficiency_level`) VALUES (4, 2, 'Language', 'Effect financial moment whether. Customer your yeah account.
Floor teach wall leave garden. Political song positive place move.', 0, NULL, 'Although source citizen few.');
INSERT INTO `ems_job_post_requirement` (`requirement_id`, `job_post_id`, `requirement_type`, `requirement_description`, `is_mandatory`, `minimum_years`, `proficiency_level`) VALUES (5, 1, 'Skill', 'Gun treat ago air member health could. Lay response there most.
Nation you current idea husband certainly wear. Discover rule prove. Option ask knowledge woman hold which production possible.', 1, 55, 'Condition son sometimes.');

-- ems_job_post_benefit (5 records)
INSERT INTO `ems_job_post_benefit` (`benefit_id`, `job_post_id`, `benefit_type`, `benefit_description`) VALUES (1, 2, 'Gas system modern design start light.', 'Hope style send fly.
Everybody minute believe bar of particularly. Major card agency maintain coach think career. Paper author appear front.
Whole win near start each lose receive.');
INSERT INTO `ems_job_post_benefit` (`benefit_id`, `job_post_id`, `benefit_type`, `benefit_description`) VALUES (2, 2, 'Police attorney picture during.', NULL);
INSERT INTO `ems_job_post_benefit` (`benefit_id`, `job_post_id`, `benefit_type`, `benefit_description`) VALUES (3, 2, 'Whole seem major detail effort design.', 'Little team network from. There throw baby.
Happen investment tax hear everybody. Success crime cover listen value picture.');
INSERT INTO `ems_job_post_benefit` (`benefit_id`, `job_post_id`, `benefit_type`, `benefit_description`) VALUES (4, 1, 'Condition low part wall close indeed.', 'Nearly campaign term never. Career agreement over lot property player decision certain.
Concern score food individual exactly machine. Vote organization law deal good. Next ever east natural.');
INSERT INTO `ems_job_post_benefit` (`benefit_id`, `job_post_id`, `benefit_type`, `benefit_description`) VALUES (5, 1, 'Summer others moment.', 'Fact shoulder ground force movie. That hope tough civil six environment. Concern federal law federal.
Difficult suggest heart tend cup tend fund citizen. Exactly party yeah under financial dark sure.');

-- ems_job_application (2 records)
INSERT INTO `ems_job_application` (`application_id`, `job_post_id`, `user_id`, `cover_letter`, `resume_document_id`, `application_status`, `applied_at`, `status_updated_at`, `status_updated_by_user_id`, `notes`) VALUES (1, 2, 1, 'Over ability marriage.', 489, 'Accepted', '2024-11-19T13:49:30', '2024-09-29T22:29:04', 1, 'Window left choice find similar.');
INSERT INTO `ems_job_application` (`application_id`, `job_post_id`, `user_id`, `cover_letter`, `resume_document_id`, `application_status`, `applied_at`, `status_updated_at`, `status_updated_by_user_id`, `notes`) VALUES (2, 2, 1, 'Know data share most tree.', 39, NULL, '2026-01-12T15:40:44', '2025-03-15T07:11:05', 1, 'Trade person last special young arrive.');

-- ems_job_interview (5 records)
INSERT INTO `ems_job_interview` (`interview_id`, `application_id`, `interview_type`, `interview_round`, `scheduled_at`, `duration_minutes`, `location`, `meeting_link`, `interviewer_user_id`, `status`, `feedback`, `rating`) VALUES (1, 2, 'Video', NULL, '2024-07-30T01:51:33', 315, 'Standard blood somebody fire.', 'Plant town special.', 1, 'Rescheduled', 'Large remain picture energy.', 2.0);
INSERT INTO `ems_job_interview` (`interview_id`, `application_id`, `interview_type`, `interview_round`, `scheduled_at`, `duration_minutes`, `location`, `meeting_link`, `interviewer_user_id`, `status`, `feedback`, `rating`) VALUES (2, 2, 'Final', 720, '2025-01-11T10:24:53', 909, 'Degree necessary week in attorney baby.', 'Third send compare nice leave try.', 1, 'Completed', 'Place spend yourself place.', 2.8);
INSERT INTO `ems_job_interview` (`interview_id`, `application_id`, `interview_type`, `interview_round`, `scheduled_at`, `duration_minutes`, `location`, `meeting_link`, `interviewer_user_id`, `status`, `feedback`, `rating`) VALUES (3, 2, 'Technical', 486, '2026-02-15T21:19:01', 342, 'Party stand card special kind century.', 'Benefit stop past raise yeah site.', 1, 'Cancelled', 'Set under especially big heavy.', 1.2);
INSERT INTO `ems_job_interview` (`interview_id`, `application_id`, `interview_type`, `interview_round`, `scheduled_at`, `duration_minutes`, `location`, `meeting_link`, `interviewer_user_id`, `status`, `feedback`, `rating`) VALUES (4, 1, 'In-Person', 155, '2024-11-12T10:47:51', 850, NULL, NULL, 1, 'Cancelled', 'Baby would career support guess explain.', 1.8);
INSERT INTO `ems_job_interview` (`interview_id`, `application_id`, `interview_type`, `interview_round`, `scheduled_at`, `duration_minutes`, `location`, `meeting_link`, `interviewer_user_id`, `status`, `feedback`, `rating`) VALUES (5, 2, 'Phone Screen', 426, '2024-10-10T02:55:05', 61, 'Want sea half.', 'Receive sea yard off.', 2, 'Scheduled', 'Concern six magazine rest list who.', 2.8);

-- ems_job_post_question (2 records)
INSERT INTO `ems_job_post_question` (`question_id`, `job_post_id`, `question_text`, `question_type`, `is_required`, `order_sequence`) VALUES (1, 2, 'Partner house fill speech democratic low.', 'Multiple Choice', 1, 587);
INSERT INTO `ems_job_post_question` (`question_id`, `job_post_id`, `question_text`, `question_type`, `is_required`, `order_sequence`) VALUES (2, 1, 'Need weight kitchen peace list fire.', 'File Upload', 1, 254);

-- ems_job_application_answer (5 records)
INSERT INTO `ems_job_application_answer` (`answer_id`, `application_id`, `question_id`, `answer_text`, `answer_file_id`) VALUES (1, 2, 1, 'Value create quickly kind movie score.', 78);
INSERT INTO `ems_job_application_answer` (`answer_id`, `application_id`, `question_id`, `answer_text`, `answer_file_id`) VALUES (2, 1, 2, 'Discover PM yes.', NULL);
INSERT INTO `ems_job_application_answer` (`answer_id`, `application_id`, `question_id`, `answer_text`, `answer_file_id`) VALUES (3, 2, 1, 'Seem expert catch.', 720);
INSERT INTO `ems_job_application_answer` (`answer_id`, `application_id`, `question_id`, `answer_text`, `answer_file_id`) VALUES (4, 1, 1, 'Remain media both black.', 633);
INSERT INTO `ems_job_application_answer` (`answer_id`, `application_id`, `question_id`, `answer_text`, `answer_file_id`) VALUES (5, 1, 1, 'Out cup dinner much some character.', 561);

-- ems_community_category (5 records)
INSERT INTO `ems_community_category` (`category_id`, `community_id`, `category_name`, `description`, `icon`, `color`, `order_sequence`) VALUES (1, 1, 'Ricardo Roberts', 'Record interesting design visit. Thank high budget.
Watch matter able from water feeling. Him history manager. Mission vote add speak within not.', 'Either agreement local.', 'Live north start available level popular.', 471);
INSERT INTO `ems_community_category` (`category_id`, `community_id`, `category_name`, `description`, `icon`, `color`, `order_sequence`) VALUES (2, 1, 'Michael Peters', 'News respond player mission ball serious. Reduce article guess class before.
Science accept find kid. Wife mission foot when natural me. Adult theory sport town second upon.', 'Purpose reveal though east.', 'Method media theory election.', 314);
INSERT INTO `ems_community_category` (`category_id`, `community_id`, `category_name`, `description`, `icon`, `color`, `order_sequence`) VALUES (3, 2, 'Miguel Wood', 'Child generation use eye leave act recent. Ground price professor though.
Shoulder option wall letter avoid player. Really home office.
Talk staff short material. No difference eat west.', 'Yes study market bank wife.', 'Character language police animal picture.', 175);
INSERT INTO `ems_community_category` (`category_id`, `community_id`, `category_name`, `description`, `icon`, `color`, `order_sequence`) VALUES (4, 2, 'Lance Maxwell', 'Occur foot cold entire. However ready dinner develop college actually.', 'Movement list front lot.', 'Military husband boy.', 927);
INSERT INTO `ems_community_category` (`category_id`, `community_id`, `category_name`, `description`, `icon`, `color`, `order_sequence`) VALUES (5, 2, 'Robert Dixon', 'Lay beyond feel accept medical.
Tend modern final second network hot control account. Gas clearly charge voice win.', 'Stock turn maybe ground.', 'Rule ago subject week member.', 999);

-- ems_community_rule (5 records)
INSERT INTO `ems_community_rule` (`rule_id`, `community_id`, `rule_title`, `rule_description`, `order_sequence`) VALUES (1, 2, 'Care win forget student fill half film', 'Agency themselves threat himself deal. Police myself easy soon several own man. Trouble test big Republican beyond data.', 129);
INSERT INTO `ems_community_rule` (`rule_id`, `community_id`, `rule_title`, `rule_description`, `order_sequence`) VALUES (2, 2, 'Challenge despite meeting others get drug add', 'Memory number recognize represent that. Despite food learn activity.', 909);
INSERT INTO `ems_community_rule` (`rule_id`, `community_id`, `rule_title`, `rule_description`, `order_sequence`) VALUES (3, 1, 'Statement would among rule', 'Lot design training situation wind. Person by tend course. Begin wear give cover class other way.
Voice final produce. First suffer computer myself.', 720);
INSERT INTO `ems_community_rule` (`rule_id`, `community_id`, `rule_title`, `rule_description`, `order_sequence`) VALUES (4, 1, 'Meeting difference box', 'Describe nothing teacher near evidence source per. The account area visit age entire outside. Camera way treatment consumer join mother.
Get idea itself although. Live executive near majority.', 388);
INSERT INTO `ems_community_rule` (`rule_id`, `community_id`, `rule_title`, `rule_description`, `order_sequence`) VALUES (5, 1, 'East majority heart knowledge', 'Around world west safe common some thought would. Face without onto land record. Talk service investment possible young.', 351);

-- ems_community_event (2 records)
INSERT INTO `ems_community_event` (`event_id`, `community_id`, `event_title`, `description`, `event_type`, `start_datetime`, `end_datetime`, `location`, `meeting_link`, `max_attendees`, `organizer_user_id`) VALUES (1, 1, 'Tough town through Democrat six', 'His case once instead happy computer. Thousand positive pretty less pressure manage plan particular.
Defense weight parent.', 'Meetup', '2024-04-17T10:02:16', '2025-05-19T10:10:56', 'Difference price economic.', 'Voice dog about.', 836, 2);
INSERT INTO `ems_community_event` (`event_id`, `community_id`, `event_title`, `description`, `event_type`, `start_datetime`, `end_datetime`, `location`, `meeting_link`, `max_attendees`, `organizer_user_id`) VALUES (2, 2, 'Ten cut century natural through score month home', 'Economic increase run senior poor various raise subject. Cover enough theory shoulder. Represent military cold pressure sure alone entire little.
Turn sit protect quickly during start quite.', 'Webinar', '2025-11-17T15:40:44', '2025-03-10T07:06:24', 'Education suffer get magazine goal project.', 'Appear significant lose small property marriage.', 828, 1);

-- ems_community_event_attendee (5 records)
INSERT INTO `ems_community_event_attendee` (`attendee_id`, `event_id`, `user_id`, `rsvp_status`, `attended`) VALUES (1, 1, 2, 'Waitlist', NULL);
INSERT INTO `ems_community_event_attendee` (`attendee_id`, `event_id`, `user_id`, `rsvp_status`, `attended`) VALUES (2, 1, 1, 'Going', 0);
INSERT INTO `ems_community_event_attendee` (`attendee_id`, `event_id`, `user_id`, `rsvp_status`, `attended`) VALUES (3, 2, 2, 'Maybe', 1);
INSERT INTO `ems_community_event_attendee` (`attendee_id`, `event_id`, `user_id`, `rsvp_status`, `attended`) VALUES (4, 2, 1, 'Not Going', 0);
INSERT INTO `ems_community_event_attendee` (`attendee_id`, `event_id`, `user_id`, `rsvp_status`, `attended`) VALUES (5, 2, 1, 'Waitlist', 1);

-- ems_post_attachment (5 records)
INSERT INTO `ems_post_attachment` (`attachment_id`, `post_id`, `file_name`, `file_type`, `file_url`, `file_size_kb`, `thumbnail_url`) VALUES (1, 2, 'Kathryn Brown', 'Benefit two successful while one his.', 'http://walker.com/', 695, 'https://www.jimenez.org/');
INSERT INTO `ems_post_attachment` (`attachment_id`, `post_id`, `file_name`, `file_type`, `file_url`, `file_size_kb`, `thumbnail_url`) VALUES (2, 1, 'Amanda Nelson', 'She live direction form project concern.', 'https://www.fernandez.org/', 720, 'http://miller-salazar.com/');
INSERT INTO `ems_post_attachment` (`attachment_id`, `post_id`, `file_name`, `file_type`, `file_url`, `file_size_kb`, `thumbnail_url`) VALUES (3, 1, 'Jerry Prince', 'Rich see present apply live shoulder.', 'http://www.johnson-ramirez.org/', 524, 'http://martin.biz/');
INSERT INTO `ems_post_attachment` (`attachment_id`, `post_id`, `file_name`, `file_type`, `file_url`, `file_size_kb`, `thumbnail_url`) VALUES (4, 1, 'Christopher Nelson', 'Voice note next there.', 'https://www.rios-ramos.org/', 14, 'http://www.tucker.com/');
INSERT INTO `ems_post_attachment` (`attachment_id`, `post_id`, `file_name`, `file_type`, `file_url`, `file_size_kb`, `thumbnail_url`) VALUES (5, 2, 'Erik Rose', 'Cup religious fear they since none.', 'https://clark.org/', 14, 'http://morales.net/');

-- ems_post_tag (2 records)
INSERT INTO `ems_post_tag` (`tag_id`, `tag_name`, `description`, `usage_count`) VALUES (1, 'Jessica Williams', 'Agency marriage own opportunity anyone item cut.
Kitchen whatever surface itself tree. Congress case often than finish. Officer crime issue throughout.', 863);
INSERT INTO `ems_post_tag` (`tag_id`, `tag_name`, `description`, `usage_count`) VALUES (2, 'Lee Rosales', 'Table project hear. Both message develop section network onto church.', 898);

-- ems_post_tag_link (5 records)
INSERT INTO `ems_post_tag_link` (`link_id`, `post_id`, `tag_id`) VALUES (1, 1, 1);
INSERT INTO `ems_post_tag_link` (`link_id`, `post_id`, `tag_id`) VALUES (2, 2, 1);
INSERT INTO `ems_post_tag_link` (`link_id`, `post_id`, `tag_id`) VALUES (3, 2, 2);
INSERT INTO `ems_post_tag_link` (`link_id`, `post_id`, `tag_id`) VALUES (4, 2, 1);
INSERT INTO `ems_post_tag_link` (`link_id`, `post_id`, `tag_id`) VALUES (5, 2, 1);

-- ems_market_trend_skill_demand (5 records)
INSERT INTO `ems_market_trend_skill_demand` (`demand_id`, `trend_id`, `skill_name`, `demand_level`, `growth_rate`, `average_salary_range`, `job_openings_count`, `region`, `industry`) VALUES (1, 1, 'Kathy Peterson', 'Low', 231.77, 'Machine despite apply.', 784, 'People seven take civil.', 'Red theory black world eight.');
INSERT INTO `ems_market_trend_skill_demand` (`demand_id`, `trend_id`, `skill_name`, `demand_level`, `growth_rate`, `average_salary_range`, `job_openings_count`, `region`, `industry`) VALUES (2, 1, 'Denise Johnson', 'Very High', NULL, 'Radio happen writer better none fill.', 955, 'Pay instead begin thing interest claim.', 'Pattern share vote anyone.');
INSERT INTO `ems_market_trend_skill_demand` (`demand_id`, `trend_id`, `skill_name`, `demand_level`, `growth_rate`, `average_salary_range`, `job_openings_count`, `region`, `industry`) VALUES (3, 1, 'David Williams', 'Low', 540.84, 'Can other candidate.', 28, 'Situation police officer relationship.', 'Sign whatever eight join control.');
INSERT INTO `ems_market_trend_skill_demand` (`demand_id`, `trend_id`, `skill_name`, `demand_level`, `growth_rate`, `average_salary_range`, `job_openings_count`, `region`, `industry`) VALUES (4, 2, 'Jill Richardson', 'Very High', 153.69, 'But law our matter.', 936, 'Decide something remember.', 'Would discover how hundred station ten.');
INSERT INTO `ems_market_trend_skill_demand` (`demand_id`, `trend_id`, `skill_name`, `demand_level`, `growth_rate`, `average_salary_range`, `job_openings_count`, `region`, `industry`) VALUES (5, 1, 'Tracey Pittman', 'Low', 910.43, 'Back human street low attorney never.', 328, 'Foreign test tree computer.', 'Artist city difference clearly piece recognize.');

-- ems_market_trend_industry (5 records)
INSERT INTO `ems_market_trend_industry` (`industry_id`, `trend_id`, `industry_name`, `description`, `growth_rate`, `market_size`, `key_players`, `emerging_technologies`) VALUES (1, 2, 'Carla Ramos', 'The project author community. Fight hear force likely would.', 915.25, 'Protect population mention season.', 'Break community build owner short red.', 'Campaign guy spend future style.');
INSERT INTO `ems_market_trend_industry` (`industry_id`, `trend_id`, `industry_name`, `description`, `growth_rate`, `market_size`, `key_players`, `emerging_technologies`) VALUES (2, 1, 'Sabrina May', 'General different lose imagine. Turn many few affect hot more you. Buy job test place heavy serve door around.
Fear pick majority. Movement learn threat similar.', 356.41, 'Business sometimes note down.', 'Though should I about must.', 'Play artist will successful.');
INSERT INTO `ems_market_trend_industry` (`industry_id`, `trend_id`, `industry_name`, `description`, `growth_rate`, `market_size`, `key_players`, `emerging_technologies`) VALUES (3, 1, 'Christine Nelson', 'Security government staff. Produce training many truth. Example cost yes student region fish.
Defense take red especially. Pressure law most author.', 751.55, 'Of behind marriage.', 'Down event quickly.', 'Ball level air if.');
INSERT INTO `ems_market_trend_industry` (`industry_id`, `trend_id`, `industry_name`, `description`, `growth_rate`, `market_size`, `key_players`, `emerging_technologies`) VALUES (4, 1, 'Mark Wade', NULL, 740.29, 'Explain they full baby according.', NULL, 'Much myself move.');
INSERT INTO `ems_market_trend_industry` (`industry_id`, `trend_id`, `industry_name`, `description`, `growth_rate`, `market_size`, `key_players`, `emerging_technologies`) VALUES (5, 2, 'Stephanie Webb', 'Job seat some law. Maybe report third film. It single avoid agent ahead enter.', 419.78, 'Door within again.', 'Claim move here off condition none.', 'General show car his improve sense.');

-- ems_market_trend_location (5 records)
INSERT INTO `ems_market_trend_location` (`location_id`, `trend_id`, `country`, `region`, `city`, `job_market_health`, `unemployment_rate`, `average_salary`, `cost_of_living_index`, `top_industries`) VALUES (1, 2, 'Cook Islands', 'Member minute size.', 'South Kaylafurt', 'Good', 13.0, 'Through day report house decision bed.', 212.96, 'Success who after find mouth provide.');
INSERT INTO `ems_market_trend_location` (`location_id`, `trend_id`, `country`, `region`, `city`, `job_market_health`, `unemployment_rate`, `average_salary`, `cost_of_living_index`, `top_industries`) VALUES (2, 1, 'Micronesia', 'What control my community television.', 'Port Paulfurt', 'Fair', 734.83, 'Loss positive difference building.', 658.49, 'Fill help care into score reflect.');
INSERT INTO `ems_market_trend_location` (`location_id`, `trend_id`, `country`, `region`, `city`, `job_market_health`, `unemployment_rate`, `average_salary`, `cost_of_living_index`, `top_industries`) VALUES (3, 2, 'Kenya', 'Half arm out.', 'Kaylashire', 'Good', 345.12, 'Newspaper move follow tonight head bad gun.', 912.64, 'Hair yet support try game politics.');
INSERT INTO `ems_market_trend_location` (`location_id`, `trend_id`, `country`, `region`, `city`, `job_market_health`, `unemployment_rate`, `average_salary`, `cost_of_living_index`, `top_industries`) VALUES (4, 2, 'Slovakia (Slovak Republic)', NULL, 'Devinhaven', 'Weak', 490.13, 'South should generation accept.', 489.45, 'Candidate others identify.');
INSERT INTO `ems_market_trend_location` (`location_id`, `trend_id`, `country`, `region`, `city`, `job_market_health`, `unemployment_rate`, `average_salary`, `cost_of_living_index`, `top_industries`) VALUES (5, 2, 'Tanzania', 'Four money woman camera.', 'Port Jamie', 'Fair', 562.54, 'Mind different report likely military.', 987.89, 'Conference yard particularly.');

-- ems_user_skill_endorsement (5 records)
INSERT INTO `ems_user_skill_endorsement` (`endorsement_id`, `skill_id`, `endorsed_by_user_id`, `endorsement_comment`, `relationship`) VALUES (1, 2, 1, NULL, 'Beat remain population democratic future structure.');
INSERT INTO `ems_user_skill_endorsement` (`endorsement_id`, `skill_id`, `endorsed_by_user_id`, `endorsement_comment`, `relationship`) VALUES (2, 1, 1, 'All they necessary.', 'Civil arrive section marriage.');
INSERT INTO `ems_user_skill_endorsement` (`endorsement_id`, `skill_id`, `endorsed_by_user_id`, `endorsement_comment`, `relationship`) VALUES (3, 2, 2, NULL, 'Continue list hotel get like.');
INSERT INTO `ems_user_skill_endorsement` (`endorsement_id`, `skill_id`, `endorsed_by_user_id`, `endorsement_comment`, `relationship`) VALUES (4, 2, 2, NULL, 'Across there billion moment.');
INSERT INTO `ems_user_skill_endorsement` (`endorsement_id`, `skill_id`, `endorsed_by_user_id`, `endorsement_comment`, `relationship`) VALUES (5, 2, 1, 'Win huge peace.', 'Other bar act ahead many must.');

-- ems_user_recommendation (5 records)
INSERT INTO `ems_user_recommendation` (`recommendation_id`, `user_id`, `recommended_by_user_id`, `recommendation_text`, `relationship`, `position_at_time`, `is_visible`) VALUES (1, 2, 2, 'Democratic source ten.', 'Identify join understand bar property high.', 'Respond believe many just put right.', 1);
INSERT INTO `ems_user_recommendation` (`recommendation_id`, `user_id`, `recommended_by_user_id`, `recommendation_text`, `relationship`, `position_at_time`, `is_visible`) VALUES (2, 1, 2, 'Determine history field debate director.', 'Agree suffer just appear.', 'Congress energy population receive.', 0);
INSERT INTO `ems_user_recommendation` (`recommendation_id`, `user_id`, `recommended_by_user_id`, `recommendation_text`, `relationship`, `position_at_time`, `is_visible`) VALUES (3, 2, 2, 'Culture police lose measure.', 'Too including me sound.', 'Trade store rule ten meet.', 1);
INSERT INTO `ems_user_recommendation` (`recommendation_id`, `user_id`, `recommended_by_user_id`, `recommendation_text`, `relationship`, `position_at_time`, `is_visible`) VALUES (4, 2, 1, 'Watch case compare wrong reveal.', 'Message face material professional save.', 'Doctor discover stock risk also memory until.', 0);
INSERT INTO `ems_user_recommendation` (`recommendation_id`, `user_id`, `recommended_by_user_id`, `recommendation_text`, `relationship`, `position_at_time`, `is_visible`) VALUES (5, 1, 2, 'Know even building animal professional pretty.', 'Side any return audience college price.', 'Present important many should approach quite.', NULL);

-- ems_notification (5 records)
INSERT INTO `ems_notification` (`notification_id`, `user_id`, `notification_type`, `title`, `message`, `related_entity_type`, `related_entity_id`, `action_url`, `is_read`, `read_at`, `priority`) VALUES (1, 1, 'Yet require many.', 'Every clear practice become message voice customer', 'Out think happen candidate.', 'Act forward important run would surface rock.', 70, 'https://lopez.com/', 0, '2025-06-04T08:03:48', 'Low');
INSERT INTO `ems_notification` (`notification_id`, `user_id`, `notification_type`, `title`, `message`, `related_entity_type`, `related_entity_id`, `action_url`, `is_read`, `read_at`, `priority`) VALUES (2, 1, 'Animal near quickly population street evening.', 'Form me international population kid report', 'Look practice officer.', 'Population quickly current ask set.', 360, 'https://hernandez.info/', NULL, '2025-08-09T01:09:39', 'High');
INSERT INTO `ems_notification` (`notification_id`, `user_id`, `notification_type`, `title`, `message`, `related_entity_type`, `related_entity_id`, `action_url`, `is_read`, `read_at`, `priority`) VALUES (3, 2, 'Ever thank cold.', 'Election strong already start clear', 'Leave face manager.', 'Sometimes deal cost do prevent.', 67, NULL, 0, '2025-12-04T17:09:37', 'Urgent');
INSERT INTO `ems_notification` (`notification_id`, `user_id`, `notification_type`, `title`, `message`, `related_entity_type`, `related_entity_id`, `action_url`, `is_read`, `read_at`, `priority`) VALUES (4, 2, 'Bit thing watch audience.', 'Play Congress early American report on', 'War where practice deep from.', 'Down prevent also game save.', 853, NULL, 1, '2026-01-29T06:24:19', 'Urgent');
INSERT INTO `ems_notification` (`notification_id`, `user_id`, `notification_type`, `title`, `message`, `related_entity_type`, `related_entity_id`, `action_url`, `is_read`, `read_at`, `priority`) VALUES (5, 2, 'Eat star commercial age.', 'Law like mother charge', 'Nature national good.', 'Include type discover letter.', 878, NULL, 0, '2025-01-20T04:45:13', NULL);

-- ems_course_job_post_link (5 records)
INSERT INTO `ems_course_job_post_link` (`link_id`, `course_id`, `job_post_id`, `relevance_score`, `matching_skills`, `ai_generated`) VALUES (1, 2, 1, 0.83, '{}', 0);
INSERT INTO `ems_course_job_post_link` (`link_id`, `course_id`, `job_post_id`, `relevance_score`, `matching_skills`, `ai_generated`) VALUES (2, 1, 2, 0.52, '{}', 0);
INSERT INTO `ems_course_job_post_link` (`link_id`, `course_id`, `job_post_id`, `relevance_score`, `matching_skills`, `ai_generated`) VALUES (3, 2, 1, 0.8, '{}', NULL);
INSERT INTO `ems_course_job_post_link` (`link_id`, `course_id`, `job_post_id`, `relevance_score`, `matching_skills`, `ai_generated`) VALUES (4, 2, 2, 0.11, '{}', 0);
INSERT INTO `ems_course_job_post_link` (`link_id`, `course_id`, `job_post_id`, `relevance_score`, `matching_skills`, `ai_generated`) VALUES (5, 2, 2, 0.5, NULL, 1);

-- ems_course_community_link (5 records)
INSERT INTO `ems_course_community_link` (`link_id`, `course_id`, `community_id`, `link_type`, `is_active`) VALUES (1, 2, 2, NULL, 1);
INSERT INTO `ems_course_community_link` (`link_id`, `course_id`, `community_id`, `link_type`, `is_active`) VALUES (2, 2, 2, NULL, 0);
INSERT INTO `ems_course_community_link` (`link_id`, `course_id`, `community_id`, `link_type`, `is_active`) VALUES (3, 2, 2, NULL, 0);
INSERT INTO `ems_course_community_link` (`link_id`, `course_id`, `community_id`, `link_type`, `is_active`) VALUES (4, 1, 1, 'Study Group', 1);
INSERT INTO `ems_course_community_link` (`link_id`, `course_id`, `community_id`, `link_type`, `is_active`) VALUES (5, 2, 1, 'Alumni', 0);

-- ems_job_post_community_link (5 records)
INSERT INTO `ems_job_post_community_link` (`link_id`, `job_post_id`, `community_id`, `is_featured`, `posted_by_user_id`) VALUES (1, 1, 2, 1, 2);
INSERT INTO `ems_job_post_community_link` (`link_id`, `job_post_id`, `community_id`, `is_featured`, `posted_by_user_id`) VALUES (2, 1, 2, 0, 1);
INSERT INTO `ems_job_post_community_link` (`link_id`, `job_post_id`, `community_id`, `is_featured`, `posted_by_user_id`) VALUES (3, 1, 2, 0, 2);
INSERT INTO `ems_job_post_community_link` (`link_id`, `job_post_id`, `community_id`, `is_featured`, `posted_by_user_id`) VALUES (4, 2, 1, 0, 2);
INSERT INTO `ems_job_post_community_link` (`link_id`, `job_post_id`, `community_id`, `is_featured`, `posted_by_user_id`) VALUES (5, 1, 2, 1, 1);

-- ems_market_trend_course_link (5 records)
INSERT INTO `ems_market_trend_course_link` (`link_id`, `trend_id`, `course_id`, `relevance_score`, `demand_level`, `recommendation_reason`, `ai_generated`) VALUES (1, 1, 2, 0.5, 'Medium', 'Factor senior perhaps management.', 0);
INSERT INTO `ems_market_trend_course_link` (`link_id`, `trend_id`, `course_id`, `relevance_score`, `demand_level`, `recommendation_reason`, `ai_generated`) VALUES (2, 2, 1, 0.6, 'High', 'Young cut girl three although far.', 0);
INSERT INTO `ems_market_trend_course_link` (`link_id`, `trend_id`, `course_id`, `relevance_score`, `demand_level`, `recommendation_reason`, `ai_generated`) VALUES (3, 1, 2, 0.33, 'Medium', 'What main deal culture.', 0);
INSERT INTO `ems_market_trend_course_link` (`link_id`, `trend_id`, `course_id`, `relevance_score`, `demand_level`, `recommendation_reason`, `ai_generated`) VALUES (4, 1, 2, 0.4, 'Medium', 'Level son always oil.', 0);
INSERT INTO `ems_market_trend_course_link` (`link_id`, `trend_id`, `course_id`, `relevance_score`, `demand_level`, `recommendation_reason`, `ai_generated`) VALUES (5, 1, 2, 0.95, 'High', 'Keep skin because member.', 0);

-- ems_market_trend_job_post_link (5 records)
INSERT INTO `ems_market_trend_job_post_link` (`link_id`, `trend_id`, `job_post_id`, `relevance_score`, `growth_potential`, `salary_trend`, `ai_generated`) VALUES (1, 2, 2, 0.1, 'Very High', 'Education federal about man.', 0);
INSERT INTO `ems_market_trend_job_post_link` (`link_id`, `trend_id`, `job_post_id`, `relevance_score`, `growth_potential`, `salary_trend`, `ai_generated`) VALUES (2, 2, 1, 0.35, 'Low', 'International same hope popular region.', 1);
INSERT INTO `ems_market_trend_job_post_link` (`link_id`, `trend_id`, `job_post_id`, `relevance_score`, `growth_potential`, `salary_trend`, `ai_generated`) VALUES (3, 2, 1, 0.84, 'Low', 'Another style everything.', 0);
INSERT INTO `ems_market_trend_job_post_link` (`link_id`, `trend_id`, `job_post_id`, `relevance_score`, `growth_potential`, `salary_trend`, `ai_generated`) VALUES (4, 2, 1, NULL, 'Very High', 'Record nation American go bill.', 0);
INSERT INTO `ems_market_trend_job_post_link` (`link_id`, `trend_id`, `job_post_id`, `relevance_score`, `growth_potential`, `salary_trend`, `ai_generated`) VALUES (5, 1, 2, NULL, 'High', 'Turn affect our positive.', 0);

-- ems_market_trend_institution_link (5 records)
INSERT INTO `ems_market_trend_institution_link` (`link_id`, `trend_id`, `institution_id`, `relevance_score`, `specialization_areas`, `partnership_opportunities`, `ai_generated`) VALUES (1, 2, 2, 0.44, 'Son price six type green.', 'Drop who international grow together cold.', NULL);
INSERT INTO `ems_market_trend_institution_link` (`link_id`, `trend_id`, `institution_id`, `relevance_score`, `specialization_areas`, `partnership_opportunities`, `ai_generated`) VALUES (2, 1, 1, 0.01, 'Between single can support.', 'Top vote once mention deal.', 1);
INSERT INTO `ems_market_trend_institution_link` (`link_id`, `trend_id`, `institution_id`, `relevance_score`, `specialization_areas`, `partnership_opportunities`, `ai_generated`) VALUES (3, 2, 1, 0.26, 'Stop house record us agreement too.', 'Against establish able for school PM.', 0);
INSERT INTO `ems_market_trend_institution_link` (`link_id`, `trend_id`, `institution_id`, `relevance_score`, `specialization_areas`, `partnership_opportunities`, `ai_generated`) VALUES (4, 2, 1, 0.28, 'Four evidence eye.', 'Morning hospital court person manage.', 1);
INSERT INTO `ems_market_trend_institution_link` (`link_id`, `trend_id`, `institution_id`, `relevance_score`, `specialization_areas`, `partnership_opportunities`, `ai_generated`) VALUES (5, 1, 1, 0.42, 'Ok election right artist.', 'Bed interesting difference network sure.', 1);

-- ems_user_file (5 records)
INSERT INTO `ems_user_file` (`file_id`, `user_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_verified`, `download_count`, `thumbnail_location`) VALUES (1, 2, 'Elizabeth Ortiz', 'Crystal Robinson', 'document', 'View else be.', 'Community speak yet reduce agent.', 502, 'The compare late structure drop.', 'Adult American hotel any themselves world go. Attorney begin side section lay health point. Money fire size detail through issue.
Either well front. Knowledge yourself establish different.', 'Yet word economic.', 'Somebody system ask might staff either.', 1, 485, 'Forget together magazine item fish investment.');
INSERT INTO `ems_user_file` (`file_id`, `user_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_verified`, `download_count`, `thumbnail_location`) VALUES (2, 1, 'Alexis Phillips', 'Robert Hunter', 'markdown', 'Author watch year bi', 'Fight within speech book style watch.', 450, NULL, 'Operation political majority head high administration. Either write daughter year politics prevent later.', 'Blood water effort beautiful plant.', 'Camera economic agree.', 0, NULL, 'Catch for business because success.');
INSERT INTO `ems_user_file` (`file_id`, `user_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_verified`, `download_count`, `thumbnail_location`) VALUES (3, 1, 'Barbara Smith', 'Mark Rodriguez', 'image', 'Mr article cultural ', 'Artist eye he center school purpose third.', 965, 'Side issue level.', 'Color strong may exist. Single knowledge special size thousand own.
Century particularly source method. Pay middle true computer party market hold.', 'Across radio southern later.', NULL, 0, 882, 'Open month third arm way.');
INSERT INTO `ems_user_file` (`file_id`, `user_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_verified`, `download_count`, `thumbnail_location`) VALUES (4, 2, 'Karina Terry', 'Carrie Baldwin', 'image', NULL, 'Child today usually there difficult against.', 392, NULL, 'Reveal close painting. Per agent rise pretty customer. Trouble really recently yeah week part during.', 'Drop spend scene large.', 'Test quality outside say official.', NULL, 940, NULL);
INSERT INTO `ems_user_file` (`file_id`, `user_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_verified`, `download_count`, `thumbnail_location`) VALUES (5, 2, 'Kerri Delgado', 'Alexis Boyd', 'spreadsheet', 'Common whether whose', 'Fine up today mission.', NULL, 'Executive view foreign bed purpose.', 'Election reduce today get poor table member prepare. Exactly establish college season course fall.
Necessary although hot one final necessary change. Your game peace sign those.', NULL, 'Check check unit career.', 0, 375, 'Thus weight finish.');

-- ems_institution_file (5 records)
INSERT INTO `ems_institution_file` (`file_id`, `institution_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_verified`, `download_count`, `thumbnail_location`) VALUES (1, 1, 'Brian Floyd', 'Kelly Gentry', 'audio', 'Miss store young.', 'Avoid interesting which big worker.', 241, 'Small free answer just natural.', 'Charge decade throw respond. Type this similar big capital. Population morning dark model color loss.', 'Goal article often heart hear speak.', 'When past arrive stuff floor three.', 0, 514, 'Discover picture few ball tough.');
INSERT INTO `ems_institution_file` (`file_id`, `institution_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_verified`, `download_count`, `thumbnail_location`) VALUES (2, 2, 'Mr. Thomas Conway', 'Jessica Jones', 'html', 'Medical suggest sudd', 'Hot thought lose sense.', 714, 'Be summer late example task.', NULL, 'Popular figure deep simply.', 'Guy exactly character full.', 1, 741, 'Spend key key.');
INSERT INTO `ems_institution_file` (`file_id`, `institution_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_verified`, `download_count`, `thumbnail_location`) VALUES (3, 2, 'Justin Hughes', 'Wendy Mclean', 'presentation', NULL, 'After certain color.', 102, 'Better which grow.', 'Stuff really how small during safe body. War put grow most three evidence much. Different dinner represent worker Democrat everything cold.', 'Campaign get believe attack wife.', 'Television blood ten least why.', 0, 794, 'Form south find account make.');
INSERT INTO `ems_institution_file` (`file_id`, `institution_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_verified`, `download_count`, `thumbnail_location`) VALUES (4, 2, 'Derek Watts', 'Kelly Black', 'image', 'Human risk list char', 'Interesting daughter single term service.', 747, NULL, 'Which yard song mission impact charge decision. Research include different. Possible my sound.
Nothing employee make inside campaign market fly industry. Key standard politics.', 'Soldier house goal.', 'Medical late test thousand I.', 1, 631, 'Hold my treat.');
INSERT INTO `ems_institution_file` (`file_id`, `institution_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_verified`, `download_count`, `thumbnail_location`) VALUES (5, 1, 'Margaret Jackson', 'Dana Wright', 'audio', 'Property according c', 'Bank tend close around.', 250, 'System high religious born.', 'Amount need group deal type music Congress. Low range state democratic be type or interest.
Leader enter must dark window. Present memory fund finish she. Outside forward whom really raise.', 'Full test pick.', 'Dog usually or general onto.', 1, 574, 'Not positive environment base leave ten.');

-- ems_course_file (5 records)
INSERT INTO `ems_course_file` (`file_id`, `course_id`, `module_id`, `lesson_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_downloadable`, `requires_enrollment`, `download_count`, `thumbnail_location`, `duration_seconds`) VALUES (1, 1, 1, 1, 'Victor Byrd', 'Colin Vargas', 'image', NULL, 'Happen run turn result hand class.', NULL, 'Join them hour heavy.', 'House market career democratic though. Suddenly writer employee standard. Tell act visit Democrat.', NULL, 'Vote husband focus fish success.', NULL, 1, 913, 'There kitchen actually.', 130);
INSERT INTO `ems_course_file` (`file_id`, `course_id`, `module_id`, `lesson_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_downloadable`, `requires_enrollment`, `download_count`, `thumbnail_location`, `duration_seconds`) VALUES (2, 1, 2, 1, 'Monica Walsh', 'Thomas Martin PhD', 'spreadsheet', 'Decision view mother', 'List responsibility really whatever six bed.', 708, 'Artist bad factor goal address something.', 'Although hot which. Share yet like. Spring everything executive value picture blue.
Arm reduce fast young. Music to rest.', 'Open hand turn team during.', NULL, NULL, NULL, 267, 'May face her any material whether.', NULL);
INSERT INTO `ems_course_file` (`file_id`, `course_id`, `module_id`, `lesson_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_downloadable`, `requires_enrollment`, `download_count`, `thumbnail_location`, `duration_seconds`) VALUES (3, 2, 2, 2, 'Robin Leach', 'Sonya French', 'presentation', 'Cold science yoursel', 'Mouth attention century town.', 742, 'Turn note chance.', 'Matter billion middle our defense. Art rate process discover them everyone.
These artist dog some argue. Alone wonder drive of back ten level. Successful general nearly professor.', 'Star social experience.', 'Travel sound television TV.', 1, 0, 837, 'Exist within watch economic unit.', 18);
INSERT INTO `ems_course_file` (`file_id`, `course_id`, `module_id`, `lesson_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_downloadable`, `requires_enrollment`, `download_count`, `thumbnail_location`, `duration_seconds`) VALUES (4, 1, 1, 1, 'Stephanie Rubio', 'Chase Hansen', 'archive', 'West hard why.', 'Really early media answer north little.', 883, 'Focus wife least drop resource.', 'Film research left democratic test. Account sometimes admit song expert attack center.
Number consumer month teacher. Key structure black chair late PM.
Writer professional answer air.', 'Only factor reflect.', NULL, 0, 1, 133, 'Share of student thing turn day.', 190);
INSERT INTO `ems_course_file` (`file_id`, `course_id`, `module_id`, `lesson_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `is_downloadable`, `requires_enrollment`, `download_count`, `thumbnail_location`, `duration_seconds`) VALUES (5, 1, 2, 1, 'Dustin Newman', 'Kim Singh', 'markdown', 'They consumer some m', 'Away dinner help as.', 764, 'Among wife able worry form.', 'Understand son baby country or area. Air energy identify defense scientist. Since follow size represent eight stage expert.
Land may than cut people whatever approach. Else character next green.', 'Wear I career myself game.', 'Prevent really provide leg culture.', 0, 0, 989, NULL, 655);

-- ems_job_post_file (5 records)
INSERT INTO `ems_job_post_file` (`file_id`, `job_post_id`, `application_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `uploaded_by_user_id`, `download_count`, `thumbnail_location`) VALUES (1, 1, 1, 'Richard Bass', 'Christopher Mendez', 'spreadsheet', 'Truth himself next s', 'Maybe tree sing blue west.', 908, 'Television hour animal example main cut.', 'High authority report stuff. Mouth also majority not meeting song.', 'Dream everybody year myself so sure.', 'Trial relationship deep both.', 2, 776, 'West forward lay size.');
INSERT INTO `ems_job_post_file` (`file_id`, `job_post_id`, `application_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `uploaded_by_user_id`, `download_count`, `thumbnail_location`) VALUES (2, 1, 2, 'Jack Peck', 'Betty Mills', 'presentation', 'Too short nature fee', 'Exist both fish.', 673, 'Congress discussion toward stop.', NULL, 'Identify lose image suffer account inside.', 'Risk instead much range.', 2, 521, 'Per weight instead bag continue.');
INSERT INTO `ems_job_post_file` (`file_id`, `job_post_id`, `application_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `uploaded_by_user_id`, `download_count`, `thumbnail_location`) VALUES (3, 1, 1, 'Travis Gordon', 'Ellen Wright', 'spreadsheet', 'Activity every smile', 'Everybody sign exactly.', NULL, 'Car letter return fast.', 'Cultural necessary our. Kitchen up your north camera friend. Contain conference young also staff several.
Beautiful again book then. Industry word edge imagine.', 'Effort answer scientist.', 'Call morning enter price.', 1, 703, 'Trouble radio and natural what.');
INSERT INTO `ems_job_post_file` (`file_id`, `job_post_id`, `application_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `uploaded_by_user_id`, `download_count`, `thumbnail_location`) VALUES (4, 1, 1, 'Holly Gregory', 'Melanie Park', 'other', 'Support goal five ki', 'All most hard rather four activity.', 684, 'Authority you book who direction assume.', 'Score far bring medical civil my ball. Quite establish area our.
Throw apply relate. Source head choice.
Next knowledge rise without send. Against market suffer true.', 'Per data agent attack second.', 'Force skill quickly activity election.', 1, 775, 'Position now eat.');
INSERT INTO `ems_job_post_file` (`file_id`, `job_post_id`, `application_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `uploaded_by_user_id`, `download_count`, `thumbnail_location`) VALUES (5, 2, 1, 'Steven Jefferson', 'Steven Hart', 'pdf', 'Sell under professio', 'Car education serious.', 572, 'Her road common group exactly guy.', 'Cut wait talk receive appear test. Represent loss sea citizen ask structure.
Process may north today. Prevent lose follow spring join. Sit describe especially choice nature past western.', 'Cost message leg help.', 'Place ten wall black plan.', 2, 145, 'Hotel wish style consumer citizen measure.');

-- ems_community_file (5 records)
INSERT INTO `ems_community_file` (`file_id`, `community_id`, `post_id`, `event_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `uploaded_by_user_id`, `download_count`, `thumbnail_location`) VALUES (1, 1, 1, 2, 'Nathan Hanson', 'Matthew Barrett', 'spreadsheet', 'Off or attorney mean', 'Building not off take cut organization.', 909, 'Send better trial.', 'Few two blood exactly. They increase quality will challenge policy. Feel anyone nor work war thing citizen.
Consumer father his smile.', 'Piece over film work pretty.', NULL, 2, 951, 'Job everyone data tend.');
INSERT INTO `ems_community_file` (`file_id`, `community_id`, `post_id`, `event_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `uploaded_by_user_id`, `download_count`, `thumbnail_location`) VALUES (2, 2, 2, 1, 'Brittney Wagner DVM', 'Willie Anderson', 'audio', 'Training on probably', 'Offer option relate cultural discussion raise.', 559, 'Name actually next throw at.', 'Add claim manage effect. Stock treatment nothing during actually effort authority. Fish room capital.', 'Right radio remain run.', 'Kitchen necessary different perhaps per.', 1, 414, 'Real early second skin store.');
INSERT INTO `ems_community_file` (`file_id`, `community_id`, `post_id`, `event_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `uploaded_by_user_id`, `download_count`, `thumbnail_location`) VALUES (3, 2, 2, 2, 'Gabrielle Patel', 'Anthony Martinez', 'spreadsheet', 'Direction like last ', 'Question return young.', 532, NULL, 'Too collection firm marriage you quickly. Tax recent stay party two figure. State pass especially popular new bed total.
He perhaps any already. Charge as able current throw.', 'Institution apply card.', 'Discover someone produce.', 2, 300, 'Beyond attorney rather decade.');
INSERT INTO `ems_community_file` (`file_id`, `community_id`, `post_id`, `event_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `uploaded_by_user_id`, `download_count`, `thumbnail_location`) VALUES (4, 1, 2, 2, 'Jennifer Jones', 'Timothy Phillips', 'audio', 'Suffer court father ', 'Natural reason that there.', 547, 'During measure oil.', 'Black perform thought around power magazine watch. City social raise billion describe. Drive tree TV.
Put environment outside local car mouth anything. Weight test night leg ask piece.', 'Put contain back month.', NULL, 1, NULL, 'Law baby hospital.');
INSERT INTO `ems_community_file` (`file_id`, `community_id`, `post_id`, `event_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `uploaded_by_user_id`, `download_count`, `thumbnail_location`) VALUES (5, 1, 2, 1, 'Jennifer Pena', 'Michael Bowen', 'video', 'Forward quickly home', 'Need ten summer voice TV.', 6, 'Improve seat day front.', 'Strategy newspaper theory soon whether. Quality defense into away sometimes science.
Already case policy national wall born. Beautiful machine democratic by lead trial husband cover.', 'Popular west coach.', 'Hear set state lose or.', 2, 507, NULL);

-- ems_market_trend_file (5 records)
INSERT INTO `ems_market_trend_file` (`file_id`, `trend_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `source`, `report_date`, `download_count`, `thumbnail_location`) VALUES (1, 1, 'Amber Cline', 'Shane Ortega', 'spreadsheet', 'Court space TV.', 'Free American sometimes.', 955, 'Husband issue line everyone doctor.', 'Rich travel rate future pressure style wall. Far like full special since.
Concern reality season indeed sound strong. Four mention when knowledge with.', 'Wind risk short next put.', 'Officer would happen team six.', 'Drug very bit discuss argue.', '2023-08-17', 47, 'Throughout feeling name TV offer.');
INSERT INTO `ems_market_trend_file` (`file_id`, `trend_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `source`, `report_date`, `download_count`, `thumbnail_location`) VALUES (2, 2, 'Carlos Sawyer', 'Sophia Evans', 'video', 'Expert friend financ', 'Rock born begin.', 909, 'Room strong relate.', 'Defense yet house issue central course big. Paper end news idea similar.
Could charge every every their. Message two Democrat billion expect always.', 'Listen difficult east specific relate.', 'Very too less dream report.', 'Memory production spend.', '2023-06-24', 689, 'Top production other continue.');
INSERT INTO `ems_market_trend_file` (`file_id`, `trend_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `source`, `report_date`, `download_count`, `thumbnail_location`) VALUES (3, 2, 'Erica Ramirez', 'Julia Horn', 'archive', 'Sell middle letter p', 'Present make together particular.', 685, NULL, 'Really just include pretty. Wind quickly way explain mouth far.
Nothing and program. Team everyone middle.', 'Central which team common crime structure.', 'Certain goal according.', 'High science often sing government blood nice.', '2022-09-06', 733, NULL);
INSERT INTO `ems_market_trend_file` (`file_id`, `trend_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `source`, `report_date`, `download_count`, `thumbnail_location`) VALUES (4, 1, 'Margaret Carr', 'Maria White', 'presentation', 'Stop would really cu', 'Fine send mention.', 151, 'Threat which finish question.', 'We him student leader foreign.
Describe attention movie statement phone. Word million she pull accept. System authority act opportunity yard stop guy.', 'Concern any join training.', NULL, 'Standard yet others front player church.', '2022-10-28', 331, NULL);
INSERT INTO `ems_market_trend_file` (`file_id`, `trend_id`, `file_name`, `original_file_name`, `file_type`, `file_extension`, `file_location`, `file_size_bytes`, `mime_type`, `description`, `comment`, `category`, `source`, `report_date`, `download_count`, `thumbnail_location`) VALUES (5, 1, 'Katherine House', 'Deborah Grant', 'other', 'Suggest go education', 'Drug quality family star.', NULL, 'Role necessary heavy plan staff get on.', 'Us out interest. Shoulder form city. Once good view painting something.
Show box idea boy executive major. According from model past former. Pressure development important gas second upon.', 'Space body hear.', 'Success argue these think trouble.', 'Car spring carry.', '2022-05-22', 492, NULL);

-- system_config (5 records)
INSERT INTO `system_config` (`config_key`, `config_value`, `created_at`, `updated_at`) VALUES (NULL, 'Rest bar bed blue.', '2024-12-01T14:35:08', '2024-08-03T17:10:01');
INSERT INTO `system_config` (`config_key`, `config_value`, `created_at`, `updated_at`) VALUES ('Response dinner science.', 'Fire or bring bill keep particular.', '2024-05-10T08:15:18', '2025-03-21T05:57:09');
INSERT INTO `system_config` (`config_key`, `config_value`, `created_at`, `updated_at`) VALUES ('Hold fund black.', 'Station one enter walk color she.', '2025-05-02T06:34:51', '2024-12-02T09:46:13');
INSERT INTO `system_config` (`config_key`, `config_value`, `created_at`, `updated_at`) VALUES ('Success arrive head.', 'Own produce hear drop.', '2026-03-12T19:06:26', '2024-11-10T23:50:25');
INSERT INTO `system_config` (`config_key`, `config_value`, `created_at`, `updated_at`) VALUES ('Drop what upon rate.', 'Challenge unit industry article investment.', '2025-07-18T10:50:18', '2024-05-23T07:17:06');

-- auth_user (2 records)
INSERT INTO `auth_user` (`auth_user_id`, `username`, `email`, `password_hash`, `is_active`, `created_at`, `updated_at`) VALUES (1, 'jamesclark', 'leahbradley@example.com', '$2b$12$S0VqNtgD4HcH7SOpchZjFefMG27rMCroaM2hW37dCr14gPEWzpcXu', 1, '2025-06-19T17:28:55', '2026-03-16T11:17:25');
INSERT INTO `auth_user` (`auth_user_id`, `username`, `email`, `password_hash`, `is_active`, `created_at`, `updated_at`) VALUES (2, 'fwilson', 'adriansexton@example.com', '$2b$12$qPGbT/pbPUq881LfkVjk/OKWh/h91P/oZp2qU9LApZheud3RGSOjS', 1, '2026-02-20T22:05:06', '2025-01-20T15:14:17');

-- user_role (5 records)
INSERT INTO `user_role` (`user_role_id`, `auth_user_id`, `role`, `table_name`, `granted_at`, `granted_by_auth_user_id`) VALUES (1, 2, 'USER', 'Matthew Hancock', '2025-10-06T22:58:44', 1);
INSERT INTO `user_role` (`user_role_id`, `auth_user_id`, `role`, `table_name`, `granted_at`, `granted_by_auth_user_id`) VALUES (2, 1, 'SUPER_ADMIN', 'Matthew Cruz PhD', '2026-01-16T00:10:01', 2);
INSERT INTO `user_role` (`user_role_id`, `auth_user_id`, `role`, `table_name`, `granted_at`, `granted_by_auth_user_id`) VALUES (3, 1, 'SUPER_ADMIN', 'Stephanie Martinez', '2025-02-12T15:54:06', 2);
INSERT INTO `user_role` (`user_role_id`, `auth_user_id`, `role`, `table_name`, `granted_at`, `granted_by_auth_user_id`) VALUES (4, 2, 'SUPER_ADMIN', 'Michael Whitaker', NULL, 2);
INSERT INTO `user_role` (`user_role_id`, `auth_user_id`, `role`, `table_name`, `granted_at`, `granted_by_auth_user_id`) VALUES (5, 1, 'TABLE_ADMIN', NULL, '2025-01-05T17:02:58', 2);

-- record_owner (5 records)
INSERT INTO `record_owner` (`record_owner_id`, `auth_user_id`, `table_name`, `record_id`, `created_at`) VALUES (1, 2, 'Brandon Ballard', 1000, '2025-01-22T05:57:47');
INSERT INTO `record_owner` (`record_owner_id`, `auth_user_id`, `table_name`, `record_id`, `created_at`) VALUES (2, 1, 'Samantha Love', 495, '2025-05-28T01:37:39');
INSERT INTO `record_owner` (`record_owner_id`, `auth_user_id`, `table_name`, `record_id`, `created_at`) VALUES (3, 2, 'Kenneth Horne', 773, '2024-04-13T03:56:35');
INSERT INTO `record_owner` (`record_owner_id`, `auth_user_id`, `table_name`, `record_id`, `created_at`) VALUES (4, 1, 'Christopher James', 623, '2025-08-28T05:04:54');
INSERT INTO `record_owner` (`record_owner_id`, `auth_user_id`, `table_name`, `record_id`, `created_at`) VALUES (5, 2, 'Lisa Jimenez', 600, '2024-12-07T09:57:50');

-- query_group (2 records)
INSERT INTO `query_group` (`query_group_id`, `group_name`, `group_type`, `owner_auth_user_id`, `description`, `created_at`) VALUES (1, 'Eric Moore', 'SYSTEM', 1, 'Exactly seek interesting. Give case military somebody sure account. Million occur fact.', '2024-06-02T14:23:58');
INSERT INTO `query_group` (`query_group_id`, `group_name`, `group_type`, `owner_auth_user_id`, `description`, `created_at`) VALUES (2, 'Michael Reid', 'COMMUNITY', 1, 'Decade gun culture everybody body. General middle product rather. Far any particularly life old will grow place.', '2026-01-30T14:18:21');

-- query_group_query (5 records)
INSERT INTO `query_group_query` (`query_group_query_id`, `query_group_id`, `query_name`) VALUES (1, 1, 'Stephanie Cunningham');
INSERT INTO `query_group_query` (`query_group_query_id`, `query_group_id`, `query_name`) VALUES (2, 2, 'Christina Guzman');
INSERT INTO `query_group_query` (`query_group_query_id`, `query_group_id`, `query_name`) VALUES (3, 2, 'Sabrina Johnson');
INSERT INTO `query_group_query` (`query_group_query_id`, `query_group_id`, `query_name`) VALUES (4, 2, 'Ethan Browning');
INSERT INTO `query_group_query` (`query_group_query_id`, `query_group_id`, `query_name`) VALUES (5, 2, 'Adriana Espinoza');

-- query_group_member (5 records)
INSERT INTO `query_group_member` (`query_group_member_id`, `query_group_id`, `auth_user_id`, `joined_at`, `invited_by_auth_user_id`) VALUES (1, 2, 2, '2024-07-21T16:37:16', 2);
INSERT INTO `query_group_member` (`query_group_member_id`, `query_group_id`, `auth_user_id`, `joined_at`, `invited_by_auth_user_id`) VALUES (2, 1, 1, '2024-04-27T20:03:20', 2);
INSERT INTO `query_group_member` (`query_group_member_id`, `query_group_id`, `auth_user_id`, `joined_at`, `invited_by_auth_user_id`) VALUES (3, 2, 1, '2026-02-09T12:29:11', 1);
INSERT INTO `query_group_member` (`query_group_member_id`, `query_group_id`, `auth_user_id`, `joined_at`, `invited_by_auth_user_id`) VALUES (4, 2, 1, NULL, 2);
INSERT INTO `query_group_member` (`query_group_member_id`, `query_group_id`, `auth_user_id`, `joined_at`, `invited_by_auth_user_id`) VALUES (5, 2, 2, '2025-12-25T21:16:15', 2);

-- query_group_record (5 records)
INSERT INTO `query_group_record` (`query_group_record_id`, `query_group_id`, `table_name`, `record_id`, `added_by_auth_user_id`, `added_at`) VALUES (1, 1, 'Alexander Edwards', 53, 2, '2025-09-25T23:15:06');
INSERT INTO `query_group_record` (`query_group_record_id`, `query_group_id`, `table_name`, `record_id`, `added_by_auth_user_id`, `added_at`) VALUES (2, 1, 'Brian Ortega MD', 772, 2, '2025-04-15T22:59:05');
INSERT INTO `query_group_record` (`query_group_record_id`, `query_group_id`, `table_name`, `record_id`, `added_by_auth_user_id`, `added_at`) VALUES (3, 1, 'Joshua Strong', 904, 1, '2025-08-05T07:56:24');
INSERT INTO `query_group_record` (`query_group_record_id`, `query_group_id`, `table_name`, `record_id`, `added_by_auth_user_id`, `added_at`) VALUES (4, 2, 'Sarah Gomez', 331, 2, '2025-08-01T15:09:50');
INSERT INTO `query_group_record` (`query_group_record_id`, `query_group_id`, `table_name`, `record_id`, `added_by_auth_user_id`, `added_at`) VALUES (5, 1, 'Nicholas Reyes', 58, 1, '2025-04-24T22:34:19');

-- access_audit_log (5 records)
INSERT INTO `access_audit_log` (`audit_id`, `auth_user_id`, `action`, `table_name`, `record_id`, `access_granted`, `denial_reason`, `ip_address`, `user_agent`, `accessed_at`) VALUES (1, 1, 'Few shoulder to think.', 'Maria Chang', 495, 0, 'Them may product.', 'USNS Davis, FPO AE 99579', 'Shake arm arm through professor least.', '2025-01-31T21:10:01');
INSERT INTO `access_audit_log` (`audit_id`, `auth_user_id`, `action`, `table_name`, `record_id`, `access_granted`, `denial_reason`, `ip_address`, `user_agent`, `accessed_at`) VALUES (2, 2, 'Generation fast bed join name.', 'Anthony Walker', 298, 0, 'Whether read official south drive.', '21422 Ramirez Fords, Lake Josephburgh, TN 158', 'Mission pretty adult develop sing.', '2026-03-01T16:47:34');
INSERT INTO `access_audit_log` (`audit_id`, `auth_user_id`, `action`, `table_name`, `record_id`, `access_granted`, `denial_reason`, `ip_address`, `user_agent`, `accessed_at`) VALUES (3, 2, 'Reality ahead view above.', 'Allison Contreras', 975, 1, 'Strong always environment decision.', '3989 Bradley Village, East Adam, DE 48719', 'Lead and hit job audience speak.', '2026-03-14T23:16:21');
INSERT INTO `access_audit_log` (`audit_id`, `auth_user_id`, `action`, `table_name`, `record_id`, `access_granted`, `denial_reason`, `ip_address`, `user_agent`, `accessed_at`) VALUES (4, 1, 'Star race others.', 'Kim Martin', 193, 0, NULL, '429 Harrington Groves, East Lauraland, PR 568', 'International painting set in.', '2026-03-07T05:48:15');
INSERT INTO `access_audit_log` (`audit_id`, `auth_user_id`, `action`, `table_name`, `record_id`, `access_granted`, `denial_reason`, `ip_address`, `user_agent`, `accessed_at`) VALUES (5, 2, 'Eight difficult tough individual record oil.', 'Jennifer Russo', 249, 0, 'Just federal evidence market week adult.', '903 Wanda Harbors Suite 471, Jessicachester, ', 'Mouth new be same.', '2025-01-06T07:55:17');

-- oauth2_provider (2 records)
INSERT INTO `oauth2_provider` (`provider_id`, `provider_name`, `display_name`, `client_id`, `client_secret`, `authorization_uri`, `token_uri`, `user_info_uri`, `jwk_set_uri`, `issuer_uri`, `scope`, `is_enabled`, `created_at`, `updated_at`) VALUES (1, 'Brian Church', 'Harold Evans', 'Line right human task.', 'Human ready fact consider.', 'Pattern big product whom level owner.', 'Information page upon building explain.', NULL, 'Responsibility both perhaps.', 'Truth age think five stop.', 'Nature attorney close result challenge.', 0, '2024-05-31T21:38:40', '2024-10-08T22:14:07');
INSERT INTO `oauth2_provider` (`provider_id`, `provider_name`, `display_name`, `client_id`, `client_secret`, `authorization_uri`, `token_uri`, `user_info_uri`, `jwk_set_uri`, `issuer_uri`, `scope`, `is_enabled`, `created_at`, `updated_at`) VALUES (2, 'Jared Stout', 'Todd Torres', 'Improve night your recently focus.', 'On certainly young shake rest attention.', 'Now treat down top structure prepare whose.', 'Thousand magazine stock continue.', 'Phone base both cold design trouble.', 'Miss book catch magazine arrive.', 'Glass store feel.', 'Main large entire bag child good.', 1, '2026-01-16T00:51:06', '2025-08-25T14:20:21');

-- oauth2_linked_account (5 records)
INSERT INTO `oauth2_linked_account` (`linked_account_id`, `auth_user_id`, `provider_id`, `provider_user_id`, `provider_username`, `provider_email`, `access_token`, `refresh_token`, `token_expires_at`, `linked_at`, `last_login_at`) VALUES (1, 2, 1, 'Least add task before.', 'davidsmith', 'manndaniel@example.org', 'Artist director operation partner condition trade.', 'Doctor possible by pretty.', '2025-01-09T14:32:46', '2024-09-18T14:00:23', '2024-04-29T17:55:51');
INSERT INTO `oauth2_linked_account` (`linked_account_id`, `auth_user_id`, `provider_id`, `provider_user_id`, `provider_username`, `provider_email`, `access_token`, `refresh_token`, `token_expires_at`, `linked_at`, `last_login_at`) VALUES (2, 2, 1, 'South politics record play couple.', 'ambermata', 'monica13@example.com', 'Always arm state offer stand.', 'True so decade home president best.', '2026-03-14T21:03:02', '2024-05-08T03:52:02', '2026-01-08T15:02:30');
INSERT INTO `oauth2_linked_account` (`linked_account_id`, `auth_user_id`, `provider_id`, `provider_user_id`, `provider_username`, `provider_email`, `access_token`, `refresh_token`, `token_expires_at`, `linked_at`, `last_login_at`) VALUES (3, 2, 2, 'Thank son positive new eat.', 'morganmatthew', 'alexishughes@example.net', 'Identify far wind same between.', 'Economic network total simply wall health.', '2025-03-16T23:10:49', '2025-08-12T00:24:56', '2025-12-01T09:52:32');
INSERT INTO `oauth2_linked_account` (`linked_account_id`, `auth_user_id`, `provider_id`, `provider_user_id`, `provider_username`, `provider_email`, `access_token`, `refresh_token`, `token_expires_at`, `linked_at`, `last_login_at`) VALUES (4, 2, 1, 'Affect hot treat.', 'kimberlypennington', NULL, 'Spend or here soon attention dark.', 'Discussion material lead event bag.', '2024-06-15T07:00:12', '2024-04-07T23:05:55', '2024-06-21T02:25:50');
INSERT INTO `oauth2_linked_account` (`linked_account_id`, `auth_user_id`, `provider_id`, `provider_user_id`, `provider_username`, `provider_email`, `access_token`, `refresh_token`, `token_expires_at`, `linked_at`, `last_login_at`) VALUES (5, 2, 1, 'Become season they better despite.', 'timothyfuller', 'zachary89@example.org', 'Economic enjoy able near wind that yes.', NULL, '2026-01-26T20:59:09', NULL, '2024-12-27T17:43:06');

SET FOREIGN_KEY_CHECKS = 1;
