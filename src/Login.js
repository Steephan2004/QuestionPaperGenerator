import React, { useState } from "react";
import "./Login.css"; // Import custom CSS
import { useNavigate } from "react-router-dom";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    console.log("Submitted");
    
     // Redirect to SubjectForm page
    try {
      const response = await fetch(
        `http://192.168.0.4:8000/check/?name=${username}&password=${password}`
      );
      const jsonData = await response.json();
      console.log(jsonData);
      if (jsonData.status) {
        navigate("/SubjectForm");
      } else{
        alert("Enter correct username or password")
        
      } 

    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2 className="login-title">Login</h2>
        <div className="form-group">
          <label htmlFor="username">UserName</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="form-control"
            placeholder="Enter your username"
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="form-control"
            placeholder="Enter your password"
          />
        </div>
        <button className="login-button" onClick={handleLogin}>
          Login
        </button>
      </div>
    </div>
  );
};

export default Login;
