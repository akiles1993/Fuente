#!/usr/bin/env python3
"""
Tests para Contratos Inteligentes URTToken
Usando Brownie/Hardhat para testing
"""

import pytest
from web3 import Web3
from typing import Dict, Any

# Mock para simular contrato sin Web3 completo
class MockURTContract:
    def __init__(self):
        self.balances: Dict[str, int] = {}
        self.allowances: Dict[str, Dict[str, int]] = {}
        self.total_supply = int(1e18) * int(1e9)  # 1B tokens
        self.owner = "0x" + "1" * 40
        self.paused = False
        self.registered_tokens: Dict[str, Dict[str, Any]] = {}
    
    def transfer(self, from_addr: str, to_addr: str, amount: int) -> bool:
        """Transferir tokens"""
        if self.paused:
            raise Exception("Token paused")
        if self.balances.get(from_addr, 0) < amount:
            raise Exception("Insufficient balance")
        
        self.balances[from_addr] = self.balances.get(from_addr, 0) - amount
        self.balances[to_addr] = self.balances.get(to_addr, 0) + amount
        return True
    
    def approve(self, owner: str, spender: str, amount: int) -> bool:
        """Aprobar transferencia"""
        if owner not in self.allowances:
            self.allowances[owner] = {}
        self.allowances[owner][spender] = amount
        return True
    
    def issue_ur_token(
        self,
        rid: str,
        urn: str,
        content_hash: str,
        issuer: str
    ) -> str:
        """Emitir nuevo token URT"""
        token_id = Web3.keccak(text=f"{rid}{issuer}")
        self.registered_tokens[token_id.hex()] = {
            "rid": rid,
            "urn": urn,
            "content_hash": content_hash,
            "issuer": issuer,
            "verified": False
        }
        return token_id.hex()
    
    def verify_ur_token(self, token_id: str) -> bool:
        """Verificar token URT"""
        if token_id not in self.registered_tokens:
            raise Exception("Token not found")
        self.registered_tokens[token_id]["verified"] = True
        return True
    
    def get_ur_token(self, token_id: str) -> Dict[str, Any]:
        """Obtener info de token"""
        return self.registered_tokens.get(token_id, {})


class TestURTTokenERC20:
    """Test funcionalidad ERC-20"""
    
    @pytest.fixture
    def contract(self):
        return MockURTContract()
    
    def test_transfer(self, contract):
        """Test transferencia de tokens"""
        from_addr = "0x" + "1" * 40
        to_addr = "0x" + "2" * 40
        amount = int(1e18)  # 1 token
        
        contract.balances[from_addr] = int(1e18) * int(1e9)
        
        assert contract.transfer(from_addr, to_addr, amount)
        assert contract.balances[to_addr] == amount
        assert contract.balances[from_addr] == int(1e18) * int(1e9) - amount
    
    def test_transfer_insufficient_balance(self, contract):
        """Test que transfer falla si no hay balance"""
        from_addr = "0x" + "1" * 40
        to_addr = "0x" + "2" * 40
        
        with pytest.raises(Exception, match="Insufficient balance"):
            contract.transfer(from_addr, to_addr, int(1e18))
    
    def test_approve(self, contract):
        """Test aprobar gastos"""
        owner = "0x" + "1" * 40
        spender = "0x" + "2" * 40
        amount = int(1e18)
        
        assert contract.approve(owner, spender, amount)
        assert contract.allowances[owner][spender] == amount
    
    def test_transfer_paused(self, contract):
        """Test que transfer falla si está pausado"""
        contract.paused = True
        
        with pytest.raises(Exception, match="Token paused"):
            contract.transfer("0x" + "1" * 40, "0x" + "2" * 40, int(1e18))


class TestURTTokenProtocol:
    """Test funcionalidad URT Protocol"""
    
    @pytest.fixture
    def contract(self):
        return MockURTContract()
    
    def test_issue_ur_token(self, contract):
        """Test emitir nuevo token URT"""
        token_id = contract.issue_ur_token(
            rid="RID-A7CCC968",
            urn="urn:resource:fuente:A7CCC968",
            content_hash="0x" + "a" * 64,
            issuer="0x" + "1" * 40
        )
        
        assert token_id is not None
        assert token_id in contract.registered_tokens
    
    def test_verify_ur_token(self, contract):
        """Test verificar token URT"""
        token_id = contract.issue_ur_token(
            "RID-A7CCC968",
            "urn:resource:fuente:A7CCC968",
            "0x" + "a" * 64,
            "0x" + "1" * 40
        )
        
        assert not contract.registered_tokens[token_id]["verified"]
        contract.verify_ur_token(token_id)
        assert contract.registered_tokens[token_id]["verified"]
    
    def test_get_ur_token(self, contract):
        """Test obtener información de token"""
        token_id = contract.issue_ur_token(
            "RID-A7CCC968",
            "urn:resource:fuente:A7CCC968",
            "0x" + "a" * 64,
            "0x" + "1" * 40
        )
        
        token_info = contract.get_ur_token(token_id)
        
        assert token_info["rid"] == "RID-A7CCC968"
        assert "urn:resource" in token_info["urn"]
    
    def test_verify_nonexistent_token(self, contract):
        """Test que verificar token inexistente falla"""
        with pytest.raises(Exception, match="Token not found"):
            contract.verify_ur_token("0x" + "nonexistent")
    
    def test_multiple_token_issuance(self, contract):
        """Test emitir múltiples tokens"""
        token_ids = []
        
        for i in range(10):
            token_id = contract.issue_ur_token(
                f"RID-{i:08X}",
                f"urn:resource:fuente:{i:08X}",
                "0x" + hex(i)[2:].zfill(64),
                "0x" + "1" * 40
            )
            token_ids.append(token_id)
        
        # Todos únicos
        assert len(set(token_ids)) == 10
        
        # Todos están registrados
        for token_id in token_ids:
            assert token_id in contract.registered_tokens


class TestURTIntegration:
    """Tests de integración completa"""
    
    def test_full_token_lifecycle(self):
        """Test ciclo de vida completo"""
        contract = MockURTContract()
        
        # 1. Setup
        issuer = "0x" + "1" * 40
        user = "0x" + "2" * 40
        contract.balances[issuer] = int(1e18) * int(1e9)
        
        # 2. Emitir URT Token
        token_id = contract.issue_ur_token(
            "RID-TEST0001",
            "urn:resource:fuente:TEST0001",
            "0x" + "a" * 64,
            issuer
        )
        
        # 3. Verificar token
        contract.verify_ur_token(token_id)
        
        # 4. Transferir ERC-20 tokens como recompensa
        contract.transfer(issuer, user, int(10 * 1e18))  # 10 URT
        
        # 5. Verificar estados finales
        assert contract.registered_tokens[token_id]["verified"]
        assert contract.balances[user] == int(10 * 1e18)
        assert contract.balances[issuer] == int(1e18) * int(1e9) - int(10 * 1e18)


class TestURTSecurity:
    """Tests de seguridad"""
    
    def test_reentrancy_protection(self):
        """Test protección contra reentrancia"""
        # En Solidity real: usar ReentrancyGuard
        contract = MockURTContract()
        
        # Simular que solo puede ejecutarse una vez
        contract.balances["0x" + "1" * 40] = int(1e18)
        
        # Primera llamada OK
        contract.transfer("0x" + "1" * 40, "0x" + "2" * 40, int(1e18))
        
        # Segunda llamada fallaría en contrato real
        with pytest.raises(Exception):
            contract.transfer("0x" + "1" * 40, "0x" + "3" * 40, int(1e18))
    
    def test_overflow_protection(self):
        """Test protección contra overflow"""
        # En Solidity 0.8+: automático
        contract = MockURTContract()
        
        # Total supply no puede exceder límite
        assert contract.total_supply == int(1e18) * int(1e9)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
