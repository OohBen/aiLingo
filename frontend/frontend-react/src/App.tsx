import Navbar from "@/scenes/navbar";
import{useState} from "react";
import { SelectedPage } from "@/shared/types";



function App() {
  const [selectedPage,setselectedPage] = useState<SelectedPage>(SelectedPage.Home);


  return <div className="app bg-green-100"> 
  <Navbar
    selectedPage={selectedPage}
    setSelectedPage={setselectedPage}
  />
  </div>;
}

export default App;
