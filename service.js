async function getCreditConditions() {
  try {
    const response = await fetch("https://server.walletroom.online/condition");
    if (!response.ok) throw new Error("Network response was not ok");
    const data = await response.json();
    return data;
  } catch (error) {
    throw new Error("Failed to fetch credit conditions: " + error.message);
  }
}

export { getCreditConditions };
