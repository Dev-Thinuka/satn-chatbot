BEGIN;

TRUNCATE interactions, properties, agents, users, company_info RESTART IDENTITY CASCADE;

INSERT INTO company_info (id, about, contact, branches)
VALUES (
  uuid_generate_v4(),
  'S A Thomson Nerys & Co.  real-estate investment and advisory operating in Australia, Sri Lanka, and Dubai.',
  '{"email":"info@sathomson.com.au","phone":"+61-2-5550-0000","site":"https://sathomson.com.au"}',
  '[
     {"city":"Sydney","country":"Australia"},
     {"city":"Colombo","country":"Sri Lanka"},
     {"city":"Dubai","country":"UAE"}
   ]'::jsonb
);

INSERT INTO agents (id, name, contact_info, role) VALUES
  (uuid_generate_v4(), 'Anika Perera',       '{"email":"anika@sathomson.com.au","phone":"+61-2-5550-1001"}', 'Senior Agent'),
  (uuid_generate_v4(), 'Rohan Fernando',     '{"email":"rohan@sathomson.com.au","phone":"+94-11-555-2002"}', 'Agent'),
  (uuid_generate_v4(), 'Layla Al Mansoori',  '{"email":"layla@sathomson.com.au","phone":"+971-4-555-3003"}', 'Partner');

WITH a AS (SELECT id, name FROM agents)
INSERT INTO properties (id, title, description, price, location, features, agent_id) VALUES
  (uuid_generate_v4(), '2BR Apartment — Parramatta', 'Modern unit with river views and secure parking.', 720000.00, 'Parramatta, NSW, Australia',
     '{"type":"apartment","beds":2,"baths":1,"parking":1,"size_sqm":78,"amenities":["river_view","gym","security"]}', (SELECT id FROM a WHERE name='Anika Perera')),
  (uuid_generate_v4(), 'Townhouse  Epping', '3BR townhouse near schools and station.', 980000.00, 'Epping, NSW, Australia',
     '{"type":"townhouse","beds":3,"baths":2,"parking":1,"size_sqm":110,"amenities":["courtyard","gas_kitchen"]}', (SELECT id FROM a WHERE name='Anika Perera')),
  (uuid_generate_v4(), 'Luxury Villa  Colombo 07', '5BR villa with pool and landscaped garden.', 245000000.00, 'Colombo 07, Sri Lanka',
     '{"type":"villa","beds":5,"baths":4,"parking":2,"size_sqm":520,"amenities":["pool","staff_quarters","generator"]}', (SELECT id FROM a WHERE name='Rohan Fernando')),
  (uuid_generate_v4(), 'City Apartment  Colombo 02', '2BR apartment close to business district.', 82000000.00, 'Colombo 02, Sri Lanka',
     '{"type":"apartment","beds":2,"baths":2,"parking":1,"size_sqm":95,"amenities":["gym","rooftop","backup_power"]}', (SELECT id FROM a WHERE name='Rohan Fernando')),
  (uuid_generate_v4(), 'Beachfront Plot  Negombo', '12 perches beachfront land  investment grade.', 38000000.00, 'Negombo, Sri Lanka',
     '{"type":"land","area_perch":12,"zoning":"residential"}', (SELECT id FROM a WHERE name='Rohan Fernando')),
  (uuid_generate_v4(), 'Marina View  Dubai Marina', '1BR with marina view; excellent rental yield.', 1600000.00, 'Dubai Marina, Dubai, UAE',
     '{"type":"apartment","beds":1,"baths":1,"parking":1,"size_sqm":62,"amenities":["marina_view","pool","gym"]}', (SELECT id FROM a WHERE name='Layla Al Mansoori')),
  (uuid_generate_v4(), 'Palm Jumeirah  Garden Home', '4BR garden home; private beach access.', 13500000.00, 'Palm Jumeirah, Dubai, UAE',
     '{"type":"villa","beds":4,"baths":5,"parking":2,"size_sqm":610,"amenities":["private_beach","pool","driver_room"]}', (SELECT id FROM a WHERE name='Layla Al Mansoori')),
  (uuid_generate_v4(), 'CBD Investment  Sydney', 'Studio in CBD, high occupancy short-stay.', 520000.00, 'Sydney CBD, NSW, Australia',
     '{"type":"apartment","beds":0,"baths":1,"parking":0,"size_sqm":35,"amenities":["concierge","lift"]}', (SELECT id FROM a WHERE name='Anika Perera')),
  (uuid_generate_v4(), 'Family Home  Glen Waverley', '4BR house with large backyard and double garage.', 1450000.00, 'Glen Waverley, VIC, Australia',
     '{"type":"house","beds":4,"baths":2,"parking":2,"size_sqm":235,"amenities":["backyard","ducted_heating"]}', (SELECT id FROM a WHERE name='Anika Perera')),
  (uuid_generate_v4(), 'Office Floor  Colombo 03', 'Grade-A office floor (shell & core), 8,000 sqft.', 310000000.00, 'Colombo 03, Sri Lanka',
     '{"type":"commercial","size_sqft":8000,"parking":6,"fitout":"shell_core"}', (SELECT id FROM a WHERE name='Rohan Fernando')),
  (uuid_generate_v4(), 'Waterfront Loft  Barangaroo', 'Premium loft with harbour outlook.', 2150000.00, 'Barangaroo, NSW, Australia',
     '{"type":"apartment","beds":2,"baths":2,"parking":1,"size_sqm":105,"amenities":["harbour_view","concierge","wine_cellar"]}', (SELECT id FROM a WHERE name='Anika Perera')),
  (uuid_generate_v4(), 'Downtown  Business Bay', '2BR with canal view; near Bay Avenue.', 2100000.00, 'Business Bay, Dubai, UAE',
     '{"type":"apartment","beds":2,"baths":2,"parking":1,"size_sqm":108,"amenities":["canal_view","pool","gym"]}', (SELECT id FROM a WHERE name='Layla Al Mansoori'));

INSERT INTO users (id, name, email, phone) VALUES
  (uuid_generate_v4(), 'Ishara Jayasuriya', 'ishara@example.com', '+94-77-000-1111'),
  (uuid_generate_v4(), 'Aiden Clark',       'aiden@example.com',  '+61-400-222-333'),
  (uuid_generate_v4(), 'Fatima Noor',       'fatima@example.com', '+971-50-444-555');

INSERT INTO interactions (id, user_id, query_text, response_text, lang)
SELECT uuid_generate_v4(), u.id,
       'Looking for 2BR in Sydney with parking',
       'Shared shortlist of 2BR in Parramatta and Barangaroo.',
       'en'
FROM users u WHERE u.email='aiden@example.com';

COMMIT;
