import React, { useState } from 'react';
import Layout from '@theme/Layout';
import styles from './create-book.module.css';

export default function CreateBook() {
    const [formData, setFormData] = useState({
        title: '',
        topic: '',
        target_audience: '',
        chapterCount: 3
    });
    const [status, setStatus] = useState('idle'); // idle, loading, success, error

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setStatus('loading');

        // Auto-generate chapter outlines based on count for simplicity
        // In a real app, we'd ask the user or use AI to suggest them first.
        const chapters = Array.from({ length: formData.chapterCount }, (_, i) => ({
            title: `Chapter ${i + 1}: Generated Title`,
            description: `Detailed exploration of concepts related to ${formData.topic} for ${formData.target_audience}.`
        }));

        const payload = {
            title: formData.title,
            topic: formData.topic,
            target_audience: formData.target_audience,
            chapters: chapters
        };

        try {
            const response = await fetch('http://localhost:8000/book/create', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) throw new Error('Failed to start generation');

            setStatus('success');
        } catch (error) {
            console.error(error);
            setStatus('error');
        }
    };

    return (
        <Layout title="Create New Book" description="Generate a book with AI">
            <div className={styles.container}>
                <h1>Create a New Book</h1>
                <p>Enter the details below to start the AI Agentic workflow.</p>

                <form onSubmit={handleSubmit} className={styles.form}>
                    <div className={styles.group}>
                        <label>Book Title</label>
                        <input name="title" required value={formData.title} onChange={handleChange} placeholder="e.g. The Future of Retrieval Augmented Generation" />
                    </div>

                    <div className={styles.group}>
                        <label>Topic</label>
                        <input name="topic" required value={formData.topic} onChange={handleChange} placeholder="e.g. AI Agents" />
                    </div>

                    <div className={styles.group}>
                        <label>Target Audience</label>
                        <input name="target_audience" required value={formData.target_audience} onChange={handleChange} placeholder="e.g. Senior Engineers" />
                    </div>

                    <div className={styles.group}>
                        <label>Number of Chapters</label>
                        <input type="number" name="chapterCount" min="1" max="10" value={formData.chapterCount} onChange={handleChange} />
                    </div>

                    <button type="submit" disabled={status === 'loading'} className={styles.button}>
                        {status === 'loading' ? 'Generating...' : 'Start Generation Agent'}
                    </button>
                </form>

                {status === 'success' && (
                    <div className={styles.success}>
                        <h3>🚀 Generation Started!</h3>
                        <p>The AI is now writing your chapters in the background.</p>
                        <p>Check the <strong>Docs</strong> tab in a few minutes to see the new files appearing.</p>
                    </div>
                )}

                {status === 'error' && (
                    <div className={styles.error}>
                        <p>Error connecting to Backend. Is it running on port 8000?</p>
                    </div>
                )}
            </div>
        </Layout>
    );
}
