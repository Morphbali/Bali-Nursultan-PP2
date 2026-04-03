CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE(id INT, username VARCHAR, phone VARCHAR)
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM contacts
    WHERE username ILIKE '%' || pattern || '%'
       OR phone LIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

SELECT * FROM search_contacts('Ali');

CREATE OR REPLACE FUNCTION get_contacts_paginated(lim INT, off INT)
RETURNS TABLE(id INT, username VARCHAR, phone VARCHAR)
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM contacts
    ORDER BY id
    LIMIT lim OFFSET off;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM get_contacts_paginated(2, 0);