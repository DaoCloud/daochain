pragma solidity ^0.4.2;

/*import {DaoHubAccount} from 'DaoHubAccount.sol';*/

contract DaoHubVerify {
    address daocloud;
    function DaoHubVerify(){
        daocloud = msg.sender;
    }

    struct Image {
        uint imageHash;
        address owner;
        bytes repoTag;
        uint imageId;
        // bool exist;
    }

    mapping(address => mapping(bytes => Image)) ownerIdImageMap;

    event regImage(uint imageHash,
                   address owner,
                   bytes repoTag,
                   uint imageId);

    function registerImage(uint imageHash,
                           bytes repoTag,
                           uint imageId){
        ownerIdImageMap[msg.sender][repoTag] = Image(imageHash, msg.sender, repoTag, imageId);
        regImage(imageHash, msg.sender, repoTag, imageId);
    }

    function queryImage(address owner, bytes repoTag)
        constant returns(uint, address, bytes, uint){
        Image memory i = ownerIdImageMap[owner][repoTag];
        return (i.imageHash, i.owner, i.repoTag, i.imageId);
    }
}
