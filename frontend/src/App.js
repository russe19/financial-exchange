import React, {useEffect, useState} from 'react';
import "./styles/App.css"
import {BrowserRouter, Routes, Route} from "react-router-dom";
import Navbar from "./components/UI/Navbar/Navbar";
import AppRouter from "./components/AppRouter";
// import {AuthContext} from "./context";
import AllCurrency from "./pages/AllCurrency";
import cors from "cors";


function App() {
  const [isAuth, setIsAuth] = useState(false)
  const [isLoading, setLoading] = useState(true)

  useEffect(() => {
    if (localStorage.getItem('auth')) {
      setIsAuth(true)
    }
    setLoading(false)
  }, [])

  return (
      // <AuthContext.Provider value={{
      //   isAuth, setIsAuth, isLoading
      // }}>
        <BrowserRouter>
            <Navbar />
            <AppRouter />
        </BrowserRouter>
      // </AuthContext.Provider>
  )
}

export default App;
