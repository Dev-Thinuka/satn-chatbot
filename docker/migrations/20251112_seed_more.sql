-- Adds diverse listings with new attributes filled
-- Agents are referenced by name -> id for convenience

WITH a_anika AS (SELECT id FROM agents WHERE name='Anika Perera' LIMIT 1),
     a_rohan AS (SELECT id FROM agents WHERE name='Rohan Fernando' LIMIT 1),
     a_layla AS (SELECT id FROM agents WHERE name='Layla Al Mansoori' LIMIT 1)

INSERT INTO properties
(id, title, description, price, price_from, location, features, agent_id,
 beds, baths, car_spaces, est_completion,
 video_url, virtual_tour_url, brochure_url, floor_plan_url, price_list_url)
VALUES
-- AUSTRALIA
(uuid_generate_v4(),'Barangaroo Harbour View','Premium 2BR with harbour views', 980000, 890000,
 'Barangaroo, NSW, Australia',
 '{"type":"apartment","amenities":["harbour_view","gym","pool"],"size_sqm":86}', (SELECT id FROM a_anika),
 2, 2, 1, 'Q3 2026',
 'https://example.com/video/barangaroo.mp4',
 'https://example.com/vr/barangaroo',
 'https://example.com/brochures/barangaroo.pdf',
 'https://example.com/floor/barangaroo.pdf',
 'https://example.com/price/barangaroo.pdf'),

(uuid_generate_v4(),'Epping Garden Townhouse','Family townhouse close to schools', 1250000, 1150000,
 'Epping, NSW, Australia',
 '{"type":"townhouse","amenities":["yard","garage"],"size_sqm":140}', (SELECT id FROM a_anika),
 3, 2, 2, 'Completed',
 NULL, NULL,
 'https://example.com/brochures/epping.pdf',
 NULL, NULL),

-- SRI LANKA
(uuid_generate_v4(),'Ocean Breeze Colombo 03','High-rise 3BR with sea view', 145000000, 132000000,
 'Colombo 03, Sri Lanka',
 '{"type":"apartment","amenities":["sea_view","backup_power","pool"],"size_sqm":120}', (SELECT id FROM a_rohan),
 3, 3, 1, 'Q4 2027',
 'https://example.com/video/col3.mp4',
 NULL,
 NULL,
 'https://example.com/floor/col3.pdf',
 'https://example.com/price/col3.pdf'),

(uuid_generate_v4(),'Rajagiriya Sky Homes','New launch near Parliament', 95000000, 88000000,
 'Rajagiriya, Sri Lanka',
 '{"type":"apartment","amenities":["rooftop","gym"],"size_sqm":95}', (SELECT id FROM a_rohan),
 2, 2, 1, 'Q2 2026',
 NULL, 'https://example.com/vr/rajagiriya',
 'https://example.com/brochures/rajagiriya.pdf',
 NULL, NULL),

-- DUBAI / UAE
(uuid_generate_v4(),'Marina Sky Residence','Waterfront living in Dubai Marina', 2450000, 2300000,
 'Dubai Marina, Dubai, UAE',
 '{"type":"apartment","amenities":["marina_view","concierge","pool"],"size_sqm":110}', (SELECT id FROM a_layla),
 2, 2, 1, 'Ready',
 'https://example.com/video/marina.mp4',
 'https://example.com/vr/marina',
 NULL, NULL, 'https://example.com/price/marina.pdf'),

(uuid_generate_v4(),'Meydan Gated Villas','Spacious 4BR villa with garden', 5200000, 4950000,
 'Meydan, Dubai, UAE',
 '{"type":"villa","amenities":["garden","maid_room","garage"],"plot_sqm":420}', (SELECT id FROM a_layla),
 4, 4, 2, 'Q1 2027',
 NULL, NULL, 'https://example.com/brochures/meydan.pdf', NULL, NULL);
