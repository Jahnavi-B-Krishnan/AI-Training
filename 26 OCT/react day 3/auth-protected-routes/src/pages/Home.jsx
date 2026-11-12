import {Link} from "react-router-dom";

export default function Home(){
    return (
        <div className="conatiner">
            <h1>Authentication DEmo</h1>
            <p>Learn how React protects private pages</p>

            <nav>
                <Link to="/login">Login</Link>
                {"|"}
                <Link to="/dashboard">Open Dashboard</Link>
                {"|"}
                <Link to ="/about">About</Link>
            </nav>
        </div>
    )
}