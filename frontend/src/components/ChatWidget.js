import React, { useState, useEffect, useRef } from 'react';
import './ChatWidget.css'; // We'll create this css

const ChatWidget = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([]);
    const [inputValue, setInputValue] = useState('');
    const [selectedText, setSelectedText] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const messagesEndRef = useRef(null);

    // Auto-scroll to bottom
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // Listen for selection
    useEffect(() => {
        const handleMouseUp = () => {
            const selection = window.getSelection().toString().trim();
            if (selection.length > 0) {
                setSelectedText(selection);
            } else {
                // Only clear if we click outside chat widget? 
                // For now, let's keep it until manually cleared or used.
            }
        };
        document.addEventListener('mouseup', handleMouseUp);
        return () => document.removeEventListener('mouseup', handleMouseUp);
    }, []);

    const sendMessage = async () => {
        if (!inputValue.trim()) return;

        const userMsg = { role: 'user', content: inputValue, context: selectedText };
        setMessages(prev => [...prev, userMsg]);
        setInputValue('');
        setIsLoading(true);

        // Clear selection after sending?
        // setSelectedText(''); 

        try {
            const response = await fetch('http://localhost:8000/rag/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    messages: [{ role: 'user', content: userMsg.content }],
                    context_text: userMsg.context
                })
            });

            const data = await response.json();
            setMessages(prev => [...prev, { role: 'assistant', content: data.reply }]);
        } catch (error) {
            setMessages(prev => [...prev, { role: 'assistant', content: 'Error connecting to AI.' }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <>
            <div className="chat-trigger" onClick={() => setIsOpen(!isOpen)}>
                {isOpen ? '✕' : '💬 AI Chat'}
            </div>

            {isOpen && (
                <div className="chat-window">
                    <div className="chat-header">
                        <h3>Ask the Book</h3>
                    </div>

                    <div className="chat-messages">
                        {messages.map((msg, idx) => (
                            <div key={idx} className={`message ${msg.role}`}>
                                {msg.role === 'user' && msg.context && (
                                    <div className="context-quote">
                                        <strong>Selected:</strong> "{msg.context.substring(0, 50)}..."
                                    </div>
                                )}
                                {msg.content}
                            </div>
                        ))}
                        {isLoading && <div className="message assistant">Typing...</div>}
                        <div ref={messagesEndRef} />
                    </div>

                    {selectedText && (
                        <div className="selection-indicator">
                            <span style={{ fontSize: '0.8rem' }}>Using selection ({selectedText.length} chars)</span>
                            <button onClick={() => setSelectedText('')} style={{ marginLeft: '5px' }}>✕</button>
                        </div>
                    )}

                    <div className="chat-input">
                        <input
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
                            placeholder="Ask a question..."
                        />
                        <button onClick={sendMessage} disabled={isLoading}>Send</button>
                    </div>
                </div>
            )}
        </>
    );
};

export default ChatWidget;
