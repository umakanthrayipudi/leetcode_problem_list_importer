"""LeetCode GraphQL API client."""
import logging
from typing import Optional

import requests

logger = logging.getLogger(__name__)


class LeetCodeAPIClient:
    """GraphQL client for LeetCode API."""

    GRAPHQL_URL = "https://leetcode.com/graphql"

    def __init__(
        self,
        session_id: str,
        csrf_token: str,
    ) -> None:
        """
        Initialize LeetCode API client.

        Args:
            session_id: LEETCODE_SESSION cookie value
            csrf_token: CSRF token for API requests
        """
        self.session_id = session_id
        self.csrf_token = csrf_token
        self._session = self._create_session()

    def _create_session(self) -> requests.Session:
        """Create and configure requests session with auth headers."""
        session = requests.Session()
        session.headers.update({
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com",
            "x-csrftoken": self.csrf_token,
        })
        session.cookies.set("LEETCODE_SESSION", self.session_id, domain="leetcode.com")
        session.cookies.set("csrftoken", self.csrf_token, domain="leetcode.com")
        return session

    def graphql_query(self, query: str, variables: dict) -> Optional[dict]:
        """
        Execute GraphQL query.

        Args:
            query: GraphQL query string
            variables: Query variables dict

        Returns:
            Response data or None on error
        """
        payload = {
            "query": query,
            "variables": variables,
        }
        try:
            resp = self._session.post(self.GRAPHQL_URL, json=payload, timeout=15)
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            logger.error("GraphQL query failed: %s", exc)
            return None

    def graphql_mutation(
        self, operation_name: str, query: str, variables: dict
    ) -> Optional[dict]:
        """
        Execute GraphQL mutation.

        Args:
            operation_name: Mutation operation name
            query: GraphQL mutation string
            variables: Mutation variables dict

        Returns:
            Response data or None on error
        """
        payload = {
            "operationName": operation_name,
            "query": query,
            "variables": variables,
        }
        try:
            resp = self._session.post(self.GRAPHQL_URL, json=payload, timeout=15)
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            logger.error("GraphQL mutation failed: %s", exc)
            return None

    def get_question_id(self, slug: str) -> Optional[str]:
        """
        Get numeric question ID from problem slug.

        Args:
            slug: Problem slug (e.g., 'two-sum')

        Returns:
            Question ID or None if not found
        """
        query = """
            query getQuestionId($titleSlug: String!) {
              question(titleSlug: $titleSlug) {
                questionId
              }
            }
        """
        resp = self.graphql_query(query, {"titleSlug": slug})
        if resp and resp.get("data"):
            return resp["data"]["question"]["questionId"]
        return None

    def add_to_favorite(self, list_id: str, question_id: str) -> bool:
        """
        Add question to favorite list.

        Args:
            list_id: Favorite list ID
            question_id: Question ID to add

        Returns:
            True if successful, False otherwise
        """
        mutation = """
            mutation addQuestionToFavorite($favoriteIdHash: String!, $questionId: String!) {
              addQuestionToFavorite(favoriteIdHash: $favoriteIdHash, questionId: $questionId) {
                ok
                error
              }
            }
        """
        resp = self.graphql_mutation(
            "addQuestionToFavorite",
            mutation,
            {
                "favoriteIdHash": list_id,
                "questionId": question_id,
            },
        )
        if resp and resp.get("data"):
            result = resp["data"].get("addQuestionToFavorite", {})
            if result.get("ok"):
                return True
            logger.warning("Add to favorite failed: %s", result.get("error"))
        return False
