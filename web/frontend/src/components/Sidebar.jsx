import React, { useState, useEffect } from 'react';


export default function Sidebar() {
  const [count, setCount] = useState(0);

  useEffect(() => { document.title = `You clicked ${count} times`; });
  return (
    <div className="sidebar">
    <div>
      <p>You clicked {count} times</p>
      <button onClick={() => setCount(count + 1)}>
        Click me
      </button>
    </div>
    </div>
  );
}