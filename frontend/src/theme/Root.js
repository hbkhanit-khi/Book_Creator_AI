import React from 'react';
import ChatWidget from '@site/src/components/ChatWidget';

// Wrapper to add ChatWidget to every page
export default function Root({ children }) {
    return (
        <>
            {children}
            <ChatWidget />
        </>
    );
}
