import * as React from 'react';
import TextField from "@mui/material/TextField"
import Button from "@mui/material/Button"
import Alert from "@mui/material/Alert"

import authService from '../services/auth.service';

export interface ILoginFormProps {
}

export default function LoginForm (props: ILoginFormProps) {
  const [username, setUsername] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [tokenPair, setTokenPair] = React.useState({});
  const [errors, setErrors] = React.useState("")

  const handleLogin = (username: string, password: string) => {
    authService.login(username, password).then(
      tokenPair => {
        setTokenPair(tokenPair)
        window.location.reload();
      }
    ).catch((err) => {
      setErrors("Login failed! Check your credentials!")
    })
  }
  
  return (
    <div>
      { errors ? <Alert severity="error">{errors}</Alert> : <></> }
      <TextField 
        label="Username" 
        onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
          setUsername(event.target.value);
        }}
        ></TextField>
      <TextField 
        label="Password"
        type="password"
        onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
          setPassword(event.target.value);
        }}
      >
      </TextField>
      <Button variant="contained" onClick={() => {handleLogin(username, password)}}>Login</Button>
    </div>
  );
}
