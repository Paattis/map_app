import React, { useEffect, useState } from "react";
import logo from "./logo.svg";
import "./App.css";
import UserService from "./services/user.service";
import AuthService from "./services/auth.service";
import LoginForm from "./components/loginForm";
import { User } from "./classes/user";
import Button from "@mui/material/Button";
import MapView from "./components/mapView";
import { UserPoint } from "./classes/userpoint";
import UserPointService from "./services/userpoint.service";

function App() {
  const [token, setToken] = useState(() => {
    return localStorage.getItem("token");
  });
  const [user, setUser] = useState<User | null>(null);

  const [userPoints, setUserPoints] = useState<Array<UserPoint>>([]);

  const logOut = () => {
    AuthService.logOut();
    window.location.reload();
  };

  useEffect(() => {
    UserPointService.fetchUserPoints().then((data) => setUserPoints(data));
  }, []);

  useEffect(() => {
    UserService.fetchUserData().then((user) => {
      setUser(user);
    });
  }, [token]);

  return (
    <div className="App">
      <h1>Map application</h1>
      {!user ? (
        <LoginForm />
      ) : (
        <>
          <h1>Welcome {user.email}</h1>
          <Button variant="contained" onClick={logOut}>
            Log out
          </Button>
        </>
      )}
      <MapView userPoints={userPoints} user={user}></MapView>
    </div>
  );
}

export default App;
