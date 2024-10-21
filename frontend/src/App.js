import React, { useEffect, useState } from 'react';
import axios from 'axios';

const App = () => {
    const [sessionId, setSessionId] = useState('');
    const [itemName, setItemName] = useState('');
    const [itemQuantity, setItemQuantity] = useState('');
    const [shoppingCart, setShoppingCart] = useState([]);

    useEffect(() => {
        const fetchSessionId = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/shopping/session-id/', {
                    withCredentials: true,
                });
                setSessionId(response.data.session_id);
                console.log('Session ID set:', response.data.session_id);
            } catch (error) {
                console.error('Error fetching session ID:', error);
            }
        };

        fetchSessionId();
        fetchShoppingCart();
    }, []);

    const fetchShoppingCart = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/shopping/items/', {
                withCredentials: true,
            });
            setShoppingCart(response.data); 
        } catch (error) {
            console.error('Error fetching shopping cart:', error);
        }
    };

    const addItemToCart = async () => {
        try {
            const payload = { name: itemName, quantity: itemQuantity };
            await axios.post('http://127.0.0.1:8000/shopping/items/', payload, {
                withCredentials: true,
            });
            fetchShoppingCart();
        } catch (error) {
            console.error('Error adding item to cart:', error);
        }
    };

    return (
        <div style={styles.container}>
            <div style={styles.card}>
                <h3 style={styles.sessionId}>Session ID: {sessionId}</h3>
                <input
                    type="text"
                    value={itemName}
                    onChange={(e) => setItemName(e.target.value)}
                    placeholder="Item Name"
                    style={styles.input}
                />
                <input
                    type="number"
                    value={itemQuantity}
                    onChange={(e) => setItemQuantity(e.target.value)}
                    placeholder="Quantity"
                    style={styles.input}
                />
                <button onClick={addItemToCart} style={styles.button}>Add Item</button>

                <h2>Shopping Cart</h2>
                <table style={styles.table}>
                    <tbody>
                        {shoppingCart.length === 0 ? 'Empty cart' : shoppingCart.map((item) => (
                            <tr key={item.reservation_id} style={styles.tableRow}>
                                <td><b>{item.name}</b></td>
                                <td>{item.description}</td>
                                <td>{item.reservation_id}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

const styles = {
    container: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        backgroundColor: '#f0f0f0',
    },
    card: {
        backgroundColor: '#fff',
        padding: '20px',
        borderRadius: '10px',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
        textAlign: 'center',
        width: '300px',
    },
    sessionId: {
        fontSize: '14px',
        marginBottom: '20px',
    },
    input: {
        width: '90%',
        padding: '10px',
        margin: '10px 0',
        borderRadius: '5px',
        border: '1px solid #ccc',
    },
    button: {
        padding: '10px 20px',
        backgroundColor: '#007bff',
        color: '#fff',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
    },
    table: {
        width: '100%',
        borderCollapse: 'collapse',
        marginTop: '10px',
    },
    tableHeader: {
        backgroundColor: '#f8f9fa',
        padding: '10px',
        borderBottom: '2px solid #dee2e6',
    },
    tableRow: {
        borderBottom: '1px solid #dee2e6',
    },
};

export default App;
