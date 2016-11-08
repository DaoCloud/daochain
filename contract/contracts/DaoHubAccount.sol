pragma solidity ^0.4.2;

contract DaoHubAccount{
    address public daocloud;
    function DaoHubAccount(){
        daocloud = msg.sender;
    }

    mapping(address => bytes)    addrUserMap;
    mapping(bytes => address[5])  userAddrsMap;

    modifier onlyDaocloud() {
        if (msg.sender != daocloud) throw;
        _;
    }


    function bindAddr(address addr, bytes user) onlyDaocloud returns(uint){
        addrUserMap[addr] = user;
        bool flag=true;
        for (uint i=0; i<5; i++){
          if(userAddrsMap[user][i]==addr) return 2; // already exist
          if(userAddrsMap[user][i]==0){
            userAddrsMap[user][i] = addr;
            flag = false;
            break;
          }
        }
        if(flag) return 1; // array full
        return 0;
    }

    function deleteAddr(address addr, bytes user) onlyDaocloud returns(uint){
        delete addrUserMap[addr];
        bool flag=true;
        for (uint i=0; i<userAddrsMap[user].length; i++){
            if(userAddrsMap[user][i] == addr){
              userAddrsMap[user][i] = 0;
              flag = false;
              break;
            }
        }
        if(flag) return 1; // addr not in array
        return 0;
    }

    function queryByAddr(address addr) constant returns(bytes){
        return addrUserMap[addr];
    }

    function queryByUser(bytes user) constant returns(address[5]){
        return userAddrsMap[user];
    }

}
