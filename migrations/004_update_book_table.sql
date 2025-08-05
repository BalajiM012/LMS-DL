-- Migration script to update book table with missing columns

ALTER TABLE book ADD COLUMN category VARCHAR(100);
ALTER TABLE book ADD COLUMN total_quantity INTEGER DEFAULT 1;
ALTER TABLE book ADD COLUMN available_quantity INTEGER DEFAULT 1;
ALTER TABLE book ADD COLUMN description TEXT;
