import "./App.css";
import HttpCall from "./components/HttpCall";
import WebSocketCall from "./components/WebSocketCall";
import TweetViewer from "./components/TweetViewer";
import Sidebar from "./components/Sidebar";
import { io } from "socket.io-client";
import { useEffect, useState } from "react";

function App() {
  const [socketInstance, setSocketInstance] = useState("");
  const [loading, setLoading] = useState(true);
  const [buttonStatus, setButtonStatus] = useState(false);
  const topic = 'explicit';
  const scope = 'day';
  const handleClick = () => {
    if (buttonStatus === false) {
      setButtonStatus(true);
    } else {
      setButtonStatus(false);
    }
  };

  useEffect(() => {
    if (buttonStatus === true) {
      const socket = io("127.0.0.1:5001/", {
        transports: ["websocket"],
        cors: {
          origin: "http://localhost:3000/",
        },
      });

      setSocketInstance(socket);

      socket.on("connect", (data) => {
        console.log(data);
      });

      setLoading(false);
      console.log('loading',loading)
      socket.on("disconnect", (data) => {
        console.log(data);
      });

      return function cleanup() {
        socket.disconnect();
      };
    }
  }, [buttonStatus]);

  return (
    <div className="App">
      <Sidebar></Sidebar>
      <div className='right'>
      
        <div className='navbar'>
        {!buttonStatus ? (
            <button onClick={handleClick}>Connect</button>
          ) : (
            <>
              <button onClick={handleClick}>Disconnect</button>
            </>
          )}
        </div>
        <div className='sep'>
          <p>This is a sub navbar</p>
        </div>
        <div className="content">
          {!loading && !buttonStatus && <TweetViewer socket={socketInstance} topic={topic} scope={scope}  />}
        </div>
        {/* <div class='content'>
          <div className="line">
            <HttpCall />
          </div>
        
        </div> */}
      </div>
    </div>
  );
}

export default App;