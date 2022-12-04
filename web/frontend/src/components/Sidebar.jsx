import React, { useState, useEffect } from 'react';


export default function Sidebar( {socket }) {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    socket.on("query", (data) => {
      setMessages([...messages, data.data]);
    });
  }, [socket, messages]);


  return (
    <div className="sidebar">
    <div className='sidebar_top'>
        {/* logo */}
    </div>
    <div className='sidebar_queries'>   
    <h3>Queries</h3>
    <svg width="1108" height="1" viewBox="0 0 1108 1" fill="none" xmlns="http://www.w3.org/2000/svg">
    <line y1="0.5" x2="1108" y2="0.5" stroke="#E1E1E1"/>
    </svg>
    <ul>
        {messages.map((message, ind) => {
          return <li key={ind}>{message}</li>;
        })}
      </ul>
    </div>
    </div>
  );
}