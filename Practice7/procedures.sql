CREATE OR REPLACE PROCEDURE insert_or_update_user(p_username TEXT, p_phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE username = p_username) THEN
        UPDATE contacts
        SET phone = p_phone
        WHERE username = p_username;
    ELSE
        INSERT INTO contacts(username, phone)
        VALUES (p_username, p_phone);
    END IF;
END;
$$;

CALL insert_or_update_user('Nursultan', '87099999999');

CREATE OR REPLACE PROCEDURE insert_many_users(names TEXT[], phones TEXT[])
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP
        IF length(phones[i]) >= 10 THEN
            INSERT INTO contacts(username, phone)
            VALUES (names[i], phones[i])
            ON CONFLICT (phone) DO NOTHING;
        ELSE
            RAISE NOTICE 'Invalid phone: %', phones[i];
        END IF;
    END LOOP;
END;
$$;

CALL insert_many_users(
    ARRAY['A', 'B'],
    ARRAY['87011111111', '123']
);

CREATE OR REPLACE PROCEDURE delete_contact(p_value TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM contacts
    WHERE username = p_value OR phone = p_value;
END;
$$;

CALL delete_contact('Ali');