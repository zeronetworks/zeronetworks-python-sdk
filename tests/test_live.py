"""Live integration tests – run against a real Zero Networks API.

These tests are skipped by default. To enable them:

    export ZERONETWORKS_LIVE=1
    export ZERONETWORKS_API_KEY=<your-api-key>
    export ZERONETWORKS_SERVER_URL=https://portal-dev.zeronetworks.com/api/v1  # optional
    export ZN_ASSET_FQDN_1=rdc01.domain.local
    export ZN_ASSET_FQDN_2=ts01.domain.local
    export ZN_USER_ID=u:i:AbCd1234      # optional, defaults to any-user group

    python -m pytest tests/test_live.py -v

Every test that creates a resource cleans it up in a finally block (or via a
pytest fixture that yields and tears down), so the tests leave no debris in
the tenant even on failure.
"""

import pytest
from zeronetworks import Zeronetworks, errors
from zeronetworks.models import PortsList
from tests.conftest import LIVE_USER_ID

# All tests in this module require the live marker
pytestmark = pytest.mark.live


# ---------------------------------------------------------------------------
# Assets
# ---------------------------------------------------------------------------

class TestLiveAssets:
    def test_search_known_asset(self, live_client, live_asset_ids):
        asset_id, _ = live_asset_ids
        assert asset_id.startswith("a:")

    def test_search_unknown_fqdn_returns_no_id(self, live_client):
        res = live_client.assets.assets_search(fqdn="this.host.does.not.exist.invalid")
        assert res.asset_id is None

    def test_search_without_fqdn(self, live_client):
        # Should not raise; the API may return None or the first asset.
        res = live_client.assets.assets_search()
        assert res is not None


# ---------------------------------------------------------------------------
# Custom Groups  (full create → get → update → delete lifecycle)
# ---------------------------------------------------------------------------

@pytest.fixture
def live_custom_group(live_client):
    """Create a temporary custom group and delete it after the test."""
    res = live_client.groups_custom.custom_groups_create(
        name="[pytest] Temp Group",
        description="Created by the automated test suite – safe to delete",
    )
    group_id = res.entity.id
    yield res
    try:
        live_client.groups_custom.custom_groups_delete(id=group_id)
    except Exception:
        pass  # already deleted by the test itself


class TestLiveCustomGroups:
    def test_create_and_get(self, live_client, live_custom_group):
        group_id = live_custom_group.entity.id
        res = live_client.groups_custom.custom_groups_get(id=group_id)
        assert res.entity is not None
        assert res.entity.id == group_id

    def test_update_name(self, live_client, live_custom_group):
        group_id = live_custom_group.entity.id
        res = live_client.groups_custom.custom_groups_update(
            id=group_id,
            name="[pytest] Temp Group (updated)",
            description="Updated by automated test suite",
        )
        assert res.entity is not None
        assert res.entity.id == group_id

    def test_add_and_remove_member(self, live_client, live_asset_ids, live_custom_group):
        group_id = live_custom_group.entity.id
        asset_id, _ = live_asset_ids

        live_client.groups_custom.custom_groups_members_add(
            id=group_id, members_id=[asset_id]
        )
        members = live_client.groups_custom.custom_group_members_list(id=group_id)
        assert asset_id in (members.members_id or [])

        live_client.groups_custom.custom_groups_members_delete(
            id=group_id, members_id=[asset_id]
        )

    def test_delete(self, live_client):
        res = live_client.groups_custom.custom_groups_create(
            name="[pytest] Delete Me",
        )
        group_id = res.entity.id
        live_client.groups_custom.custom_groups_delete(id=group_id)
        # Confirm it's gone
        with pytest.raises(errors.ZeronetworksError):
            live_client.groups_custom.custom_groups_get(id=group_id)

    def test_get_nonexistent_raises(self, live_client):
        with pytest.raises(errors.ZeronetworksError):
            live_client.groups_custom.custom_groups_get(id="g:c:doesnotexist")


# ---------------------------------------------------------------------------
# AE Exclusions – inbound (create → get → delete)
# ---------------------------------------------------------------------------

@pytest.fixture
def live_ae_exclusion_inbound(live_client, live_asset_ids):
    asset_id, asset_id_2 = live_asset_ids
    res = live_client.ae_exclusions.ae_exclusions_inbound_create(
        local_entity_id=asset_id,
        local_processes_list=["*"],
        ports_list=[PortsList(protocol_type=6, ports="19999")],
        remote_entity_ids_list=[asset_id_2],
        description="[pytest] temp inbound AE exclusion",
    )
    excl_id = res.item.id
    yield res
    try:
        live_client.ae_exclusions.ae_exclusions_inbound_delete(id=excl_id)
    except Exception:
        pass


class TestLiveAEExclusionsInbound:
    def test_create_and_get(self, live_client, live_ae_exclusion_inbound):
        excl_id = live_ae_exclusion_inbound.item.id
        res = live_client.ae_exclusions.ae_exclusions_inbound_get(id=excl_id)
        assert res.item is not None
        assert res.item.id == excl_id

    def test_delete(self, live_client, live_asset_ids):
        asset_id, asset_id_2 = live_asset_ids
        res = live_client.ae_exclusions.ae_exclusions_inbound_create(
            local_entity_id=asset_id,
            local_processes_list=["*"],
            ports_list=[PortsList(protocol_type=6, ports="29998")],
            remote_entity_ids_list=[asset_id_2],
            description="[pytest] delete-me inbound AE exclusion",
        )
        excl_id = res.item.id
        live_client.ae_exclusions.ae_exclusions_inbound_delete(id=excl_id)
        with pytest.raises(errors.ZeronetworksError):
            live_client.ae_exclusions.ae_exclusions_inbound_get(id=excl_id)


# ---------------------------------------------------------------------------
# AE Exclusions – outbound (create → get → delete)
# ---------------------------------------------------------------------------

@pytest.fixture
def live_ae_exclusion_outbound(live_client, live_asset_ids):
    asset_id, asset_id_2 = live_asset_ids
    res = live_client.ae_exclusions.ae_exclusions_outbound_create(
        local_entity_id=asset_id,
        local_processes_list=["*"],
        ports_list=[PortsList(protocol_type=6, ports="19998")],
        remote_entity_ids_list=[asset_id_2],
        description="[pytest] temp outbound AE exclusion",
    )
    excl_id = res.item.id
    yield res
    try:
        live_client.ae_exclusions.ae_exclusions_outbound_delete(id=excl_id)
    except Exception:
        pass


class TestLiveAEExclusionsOutbound:
    def test_create_and_get(self, live_client, live_ae_exclusion_outbound):
        excl_id = live_ae_exclusion_outbound.item.id
        res = live_client.ae_exclusions.ae_exclusions_outbound_get(id=excl_id)
        assert res.item is not None
        assert res.item.id == excl_id


# ---------------------------------------------------------------------------
# Inbound Rules (create → get → update → delete)
# ---------------------------------------------------------------------------

@pytest.fixture
def live_inbound_rule(live_client, live_asset_ids):
    asset_id, asset_id_2 = live_asset_ids
    res = live_client.rules_inbound.inbound_rules_create(
        action=1,  # Allow
        local_entity_id=asset_id,
        local_processes_list=["*"],
        ports_list=[PortsList(protocol_type=6, ports="19997")],
        remote_entity_ids_list=[asset_id_2],
        state=2,  # Disabled – safer for test rules
        description="[pytest] temp inbound rule",
    )
    rule_id = res.item.id
    yield res
    try:
        live_client.rules_inbound.inbound_rule_delete(id=rule_id)
    except Exception:
        pass


class TestLiveRulesInbound:
    def test_create_and_get(self, live_client, live_inbound_rule):
        rule_id = live_inbound_rule.item.id
        res = live_client.rules_inbound.inbound_rule_get(id=rule_id)
        assert res.item is not None
        assert res.item.id == rule_id

    def test_update(self, live_client, live_inbound_rule, live_asset_ids):
        rule_id = live_inbound_rule.item.id
        asset_id, asset_id_2 = live_asset_ids
        res = live_client.rules_inbound.inbound_rule_update(
            id=rule_id,
            action=1,
            local_entity_id=asset_id,
            local_processes_list=["*"],
            ports_list=[PortsList(protocol_type=6, ports="19997")],
            remote_entity_ids_list=[asset_id_2],
            state=2,
            description="[pytest] updated inbound rule",
        )
        assert res.item is not None

    def test_delete(self, live_client, live_asset_ids):
        asset_id, asset_id_2 = live_asset_ids
        res = live_client.rules_inbound.inbound_rules_create(
            action=1,
            local_entity_id=asset_id,
            local_processes_list=["*"],
            ports_list=[PortsList(protocol_type=6, ports="29997")],
            remote_entity_ids_list=[asset_id_2],
            state=2,
            description="[pytest] delete-me inbound rule",
        )
        rule_id = res.item.id
        live_client.rules_inbound.inbound_rule_delete(id=rule_id)
        with pytest.raises(errors.ZeronetworksError):
            live_client.rules_inbound.inbound_rule_get(id=rule_id)


# ---------------------------------------------------------------------------
# Outbound Rules (create → get → delete)
# ---------------------------------------------------------------------------

@pytest.fixture
def live_outbound_rule(live_client, live_asset_ids):
    asset_id, asset_id_2 = live_asset_ids
    res = live_client.rules_outbound.outbound_rules_create(
        action=1,
        local_entity_id=asset_id,
        local_processes_list=["*"],
        ports_list=[PortsList(protocol_type=6, ports="19996")],
        remote_entity_ids_list=[asset_id_2],
        state=2,
        description="[pytest] temp outbound rule",
    )
    rule_id = res.item.id
    yield res
    try:
        live_client.rules_outbound.outbound_rule_delete(id=rule_id)
    except Exception:
        pass


class TestLiveRulesOutbound:
    def test_create_and_get(self, live_client, live_outbound_rule):
        rule_id = live_outbound_rule.item.id
        res = live_client.rules_outbound.outbound_rule_get(id=rule_id)
        assert res.item is not None
        assert res.item.id == rule_id

    def test_delete(self, live_client, live_asset_ids):
        asset_id, asset_id_2 = live_asset_ids
        res = live_client.rules_outbound.outbound_rules_create(
            action=1,
            local_entity_id=asset_id,
            local_processes_list=["*"],
            ports_list=[PortsList(protocol_type=6, ports="29996")],
            remote_entity_ids_list=[asset_id_2],
            state=2,
            description="[pytest] delete-me outbound rule",
        )
        rule_id = res.item.id
        live_client.rules_outbound.outbound_rule_delete(id=rule_id)
        with pytest.raises(errors.ZeronetworksError):
            live_client.rules_outbound.outbound_rule_get(id=rule_id)


# ---------------------------------------------------------------------------
# Internal Access Policies (create → get → delete)
# ---------------------------------------------------------------------------

@pytest.fixture
def live_iap(live_client, live_asset_ids):
    asset_id, _ = live_asset_ids
    res = live_client.internal_access_policy.internal_access_policy_create(
        dst_asset_id=asset_id,
        dst_ports_list=[PortsList(protocol_type=6, ports="22")],
        dst_process_names_list=["*"],
        name="[pytest] Temp IAP",
        rule_duration=5,  # Never
        src_user_ids_list=[LIVE_USER_ID],
        state=2,  # Disabled
        description="Created by automated test suite – safe to delete",
    )
    iap_id = res.item.id
    yield res
    try:
        live_client.internal_access_policy.internal_access_policy_delete(id=iap_id)
    except Exception:
        pass


class TestLiveInternalAccessPolicy:
    def test_create_and_get(self, live_client, live_iap):
        iap_id = live_iap.item.id
        res = live_client.internal_access_policy.internal_access_policy_get(id=iap_id)
        assert res.item is not None
        assert res.item.id == iap_id

    def test_update(self, live_client, live_iap, live_asset_ids):
        iap_id = live_iap.item.id
        asset_id, _ = live_asset_ids
        res = live_client.internal_access_policy.internal_access_policy_update(
            id=iap_id,
            dst_asset_id=asset_id,
            dst_ports_list=[PortsList(protocol_type=6, ports="22")],
            dst_process_names_list=["*"],
            name="[pytest] Temp IAP (updated)",
            rule_duration=5,
            src_user_ids_list=[LIVE_USER_ID],
            state=2,
        )
        assert res.item is not None

    def test_delete(self, live_client, live_asset_ids):
        asset_id, _ = live_asset_ids
        res = live_client.internal_access_policy.internal_access_policy_create(
            dst_asset_id=asset_id,
            dst_ports_list=[PortsList(protocol_type=6, ports="22")],
            dst_process_names_list=["*"],
            name="[pytest] Delete Me IAP",
            rule_duration=5,
            src_user_ids_list=[LIVE_USER_ID],
        )
        iap_id = res.item.id
        live_client.internal_access_policy.internal_access_policy_delete(id=iap_id)
        with pytest.raises(errors.ZeronetworksError):
            live_client.internal_access_policy.internal_access_policy_get(id=iap_id)
