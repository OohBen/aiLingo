import Link from 'next/link';
import Navbar from '../components/navbar';

const Signup = () => {
    return (
        <div>
            <Navbar />
            <div className="flex-grow flex items-center justify-center">
                <h1 className="text-2xl text-center mt-4">
                    Sign Up:
                </h1>
            </div>
        </div>
    );
};

export default Signup;