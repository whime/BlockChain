pragma solidity ^0.5.0;

import "./Fundraise.sol";

/// @title 表示慈善机构
/// @author Z. ZHONG
contract Charity
{

    /// @title 慈善机构名称
    string public name;
    /// @title 慈善机构钱包地址
    address payable public charity;
    /// @title 慈善机构的所有筹款项目
    Fundraise[] public fundraises;

    constructor(string memory _charityName) public
    {
        name = _charityName;
        charity = msg.sender;
    }

    function addFundraise(Fundraise _fund) public returns(bool)
    {
        for(uint i = 0; i < fundraises.length; i++)
        {
            if(fundraises[i] == _fund)
                return false;
        }
        fundraises.push(_fund);
        return true;
    }

    function getFundraiseCount() public view returns(uint)
    {
        return fundraises.length;
    }

    /// function getFundraiseWithIndex(uint _index) public view returns(Fundraise){ return fundraises[_index];}

}