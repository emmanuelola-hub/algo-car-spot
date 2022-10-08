import { useState, useEffect } from "react";
import './App.css';
import Header from './components/Header'
import Tabs from './components/Tabs'
import { indexerClient, myAlgoConnect } from "./utils/constants";
import { buyCarAction, createcarAction, dislikeCarAction, getCarsAction, likeCarAction } from "./utils/spotter";


function App() {
  const [address, setAddress] = useState(null);
  const [cars, setCars] = useState([]);
  const [balance, setBalance] = useState(0);

  const fetchBalance = async (accountAddress) => {
    indexerClient.lookupAccountByID(accountAddress).do()
      .then(response => {
        const _balance = response.account.amount;
        setBalance(_balance);
      })
      .catch(error => {
        console.log(error);
      });
  };

  const connectWallet = async () => {
    myAlgoConnect.connect()
      .then(accounts => {
        const _account = accounts[0];
        console.log(_account)
        setAddress(_account.address);
        fetchBalance(_account.address);
        if (_account.address) getCars();
      }).catch(error => {
        console.log('Could not connect to MyAlgo wallet');
        console.error(error);
      })
  };

  const addCar = async (data) => {
    try {
      await createcarAction(address, data)    
    } catch (error) {
      console.log(error);
    } finally {
      getCars();
      fetchBalance()
    }
  };

  const getCars = async () => {
    try {
      const cars = await getCarsAction();
      if(cars)setCars(cars)
    } catch (error) {
      console.log(error);
    }
  };

  const likeCar = async (car) => {
    try {
      await likeCarAction(address, car)
    } catch (error) {
      console.log(error);
    } finally {
      getCars();
    }
  };
  const dislikeCar = async (car) => {
    try {
      await dislikeCarAction(address, car)
    } catch (error) {
      console.log(error);
    } finally {
      getCars();
    }
  };

  const buyCar = async (car) => {
    try {
      await buyCarAction(address, car)
    } catch (error) {
      console.log(error);
    } finally {
      getCars();
      fetchBalance();
    }
  };

  useEffect(() => {
    connectWallet()
  }, [])
  

  return (
<>
      <div className="container py-3">
        <Header balance={balance} />
        <Tabs
          addCar={addCar}
          cars={cars}
          buyCar={buyCar}
          likeCar={likeCar}
          dislikeCar={dislikeCar}
          address={address}
        />
      </div>
    </>
  );
}

export default App;
