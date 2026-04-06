import { createContext, useCallback, useContext, useState } from "react";

const StoreContext = createContext({
  filters: { mac: "", startTime: "", endTime: "" },
  setFilters: () => {},
  silverData: [],
  goldData: [],
  connectionStatus: "disconnected",
  setLiveData: () => {},
  setConnectionStatus: () => {},
});

export const StoreProvider = ({ children }) => {
    const [filters, setFilters] = useState({ mac: "", startTime: "", endTime: "" });
    const [silverData, setSilverData] = useState([]);
    const [goldData, setGoldData] = useState([]);
    const [connectionStatus, setConnectionStatus] = useState("disconnected");

    const setLiveData = useCallback(({ silver = null, gold = null }) => {
        if (Array.isArray(silver)) {
            setSilverData(silver);
        }
        if (Array.isArray(gold)) {
            setGoldData(gold);
        }
    }, []);

    return (
        <StoreContext.Provider
            value={{
                filters,
                setFilters,
                silverData,
                goldData,
                connectionStatus,
                setLiveData,
                setConnectionStatus,
            }}
        >
            {children}
        </StoreContext.Provider>
    );
};

export const useStore = () => useContext(StoreContext);