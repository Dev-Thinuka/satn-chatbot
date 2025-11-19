INSERT INTO agents (id, name, contact_info, role) VALUES
  (uuid_generate_v4(), 'Anika Perera', '{"email":"anika@sathomson.com.au","phone":"+61-2-5550-1001"}', 'Senior Agent'),
  (uuid_generate_v4(), 'Rohan Fernando', '{"email":"rohan@sathomson.com.au","phone":"+94-11-555-2002"}', 'Agent')
ON CONFLICT DO NOTHING;

INSERT INTO properties (id, title, description, price, location, features, agent_id)
SELECT uuid_generate_v4(), '2BR Apartment in Parramatta', 'Modern 2BR with river views', 720000.00, 'Parramatta, NSW',
       '{"type":"apartment","beds":2,"baths":1,"parking":1}', a.id
FROM agents a WHERE a.name='Anika Perera'
ON CONFLICT DO NOTHING;

INSERT INTO users (id, name, email, phone) VALUES
  (uuid_generate_v4(), 'Test User', 'user@example.com', '+61-400-000-000')
ON CONFLICT DO NOTHING;
