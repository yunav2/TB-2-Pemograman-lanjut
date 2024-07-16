CREATE DATABASE perpustakaan;

USE perpustakaan;

CREATE TABLE buku (
    id INT AUTO_INCREMENT PRIMARY KEY,
    judul VARCHAR(255),
    penulis VARCHAR(255),
    penerbit VARCHAR(255),
    tahun_terbit YEAR,
    konten TEXT,
    ikhtisar TEXT
);