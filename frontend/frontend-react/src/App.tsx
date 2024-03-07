import Navbar from "@/scenes/navbar";
import{useState} from "react";

function App() {
  const [selectedPage,setselectedPage] = useState(`home`);


  return <div className="app bg-green-100"> 
  <Navbar
    selectedPage={selectedPage}
    setSelectedPage={setselectedPage}
  />
  </div>;
}

export default App;
