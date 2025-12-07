import React, { useEffect, useState } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import styles from './my-books.module.css';

export default function MyBooks() {
    const [books, setBooks] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('http://localhost:8000/book/list')
            .then(res => res.json())
            .then(data => {
                setBooks(data);
                setLoading(false);
            })
            .catch(err => {
                console.error("Failed to fetch books", err);
                setLoading(false);
            });
    }, []);

    return (
        <Layout title="My Books" description="Manage your AI Library">
            <div className={styles.container}>
                <div className={styles.header}>
                    <h1>My Books</h1>
                    <Link to="/create-book" className={styles.createButton}>+ New Book</Link>
                </div>

                {loading && <p>Loading library...</p>}

                {!loading && books.length === 0 && (
                    <div className={styles.empty}>
                        <p>No books found. Why not generate one?</p>
                    </div>
                )}

                <div className={styles.grid}>
                    {books.map(book => (
                        <div key={book.id} className={styles.card}>
                            <h2>{book.title}</h2>
                            <div className={styles.meta}>
                                <span className={styles.tag}>{book.topic}</span>
                            </div>
                            <p className={styles.audience}>Target: {book.audience}</p>
                            <div className={styles.actions}>
                                <Link to={book.link} className={styles.readLink}>Read Book</Link>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </Layout>
    );
}
