import React, {useEffect, useState} from 'react';
import {useParams} from "react-router-dom";
import {useFetching} from "../hooks/useFetching";
import PostService from "../api/PostService";
import Loader from "../components/UI/Loader/Loader";
import Login from "./Login";
import "../styles/AppRouter.css"
import { useNavigate } from "react-router-dom";
// import PostItem from "./PostItem";
// import {CSSTransition, TransitionGroup} from "react-transition-group";

const AllCurrency = () => {
    const navigate = useNavigate()

    const [posts, setPosts] = useState({})
    const [fetchPostById, isLoading, error] = useFetching(async () => {
        const response = await PostService.getAllCurrency()
        setPosts(response)
    })

    useEffect(() => {
        fetchPostById()
    }, [])

    return (<div className="App">
        {/*{error == 'Request failed with status code 401'*/}
        {/*    ? navigate("/login")*/}
        {/*    :*/}
        {/*    <div>*/}
                {isLoading
                    ? <div style={{display: 'flex', justifyContent: 'center', marginTop: 50}}><Loader/></div>
                    : posts?.data?.data.map(post =>
                            <div className='post_curr' key={post['Currency'].id}>
                                <h3>{post['Currency'].id}</h3>
                                <p>{post['Currency'].name} - Курс: {post['Currency'].course}</p>
                            </div>
                        )
                }

        {/*    </div>*/}
        {/*}*/}
        </div>
    );
};

export default AllCurrency;