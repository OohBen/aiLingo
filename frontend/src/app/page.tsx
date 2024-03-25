import Image from "next/image";
import Navbar from './components/navbar';

export default function Home() {
  return (
    <div>
      <Navbar />
      <div className="flex-grow flex items-center justify-center">
          <h1 className="text-2xl text-center mt-4">
              Homepage
          </h1>
      </div>
    </div>
  );
}
