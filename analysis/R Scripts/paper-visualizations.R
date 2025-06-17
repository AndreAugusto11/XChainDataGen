library(ggplot2)
library(dplyr)
library(gridExtra)
library(patchwork)
library(tidyr)
library(latex2exp)
library(ggthemes)
library(scales)
library(data.table)

all_data <- fread("../data/grouped/all_ccc_protocols.csv", select = c("bridge", "src_blockchain", "dst_blockchain", "user_cost", "output_amount_usd", "amount_received_ld_usd", "amount_usd", "src_symbol", "latency"))

all_data$src_blockchain <- as.factor(all_data$src_blockchain)
all_data$dst_blockchain <- as.factor(all_data$dst_blockchain)
all_data$bridge <- as.factor(all_data$bridge)


all_data$bridge <- factor(
  all_data$bridge,
  levels = c("ccip", "cctp", "stargate_oft", "stargate_bus", "across")
)

################################################################################
#                          Ethereum <-> Avalanche                              #
################################################################################

eth_avax_data <- all_data[all_data$src_blockchain %in% c("ethereum", "avalanche") & all_data$dst_blockchain %in% c("ethereum", "avalanche"), ]

eth_avax_data$bridge <- factor(
  eth_avax_data$bridge,
  levels = c("ccip", "cctp", "stargate_oft", "stargate_bus")
)

custom_labels <- c(
  "ccip" = "Cross-Chain Interoperability Protocol (CCIP) by Chainlink",
  "cctp" = "Cross-Chain Transfer Protocol (CCTP) by Circle",
  "stargate_oft" = "Stargate (Taxi)",
  "stargate_bus" = "Stargate (Bus)"
)

custom_breaks_x <- c(0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000)

ggplot(eth_avax_data, aes(
  x = user_cost,
  y = ifelse(bridge == "across", output_amount_usd,
    ifelse(bridge == "stargate_bus", amount_received_ld_usd, amount_usd)
  ),
  color = src_blockchain
)) +
  geom_point(size = 1.5, alpha = 0.5, position = position_jitter(width = 0.1, height = 0.1)) +
  facet_wrap(
    ~bridge,
    scales = "fixed",
    ncol = 1,
    labeller = labeller(bridge = custom_labels)
  ) +
  scale_color_manual(
    values = c("ethereum" = "orange", "avalanche" = "#0072B2"),
    labels = c(TeX(r'(Ethereum $\rightarrow$ Avalanche)'), TeX(r'(Avalanche $\rightarrow$ Ethereum)')),
    name = "Transfer Direction"
  ) +
  scale_x_log10(
    limits = c(10^-2, 10^3),
    breaks = custom_breaks_x,
    labels = function(x) {
      ifelse(x < 1,
        scales::dollar_format(accuracy = 0.01)(x),
        scales::dollar_format()(x)
      )
    }
  ) +
  scale_y_log10(
    limits = c(10^-4, 10^6),
    breaks = scales::trans_breaks(log10, function(x) 10^x, 5),
    labels = function(x) {
      ifelse(x < 1,
        scales::dollar_format(accuracy = 0.0001)(x),
        scales::dollar_format()(x)
      )
    }
  ) +
  labs(
    x = "User Cost (USD)",
    y = "Value Transferred (USD)",
    color = "Source Blockchain"
  ) +
  theme_linedraw(base_family = "Times New Roman") +
  theme(
    plot.title = element_text(
      face = "bold", size = 15, hjust = 0.5, vjust = -1
    ),
    plot.margin = unit(c(0.2, 0.2, 0.2, 0.2), "cm"),
    text = element_text(family = "serif"),
    axis.title.y = element_text(size = 25, face = "bold", vjust = 1),
    axis.title.x = element_text(size = 25, face = "bold", vjust = -1),
    axis.text = element_text(size = 25, face = "bold"),
    axis.line = element_line(color = "black", linewidth = 0.2),
    panel.grid.major.y = element_blank(),
    panel.grid.major.x = element_line(
      color = "grey80", linewidth = 0.1, linetype = 2
    ),
    panel.grid.minor.x = element_blank(),
    panel.grid.minor.y = element_blank(),
    legend.title = element_text(face = "bold", size = 25),
    legend.text = element_text(size = 25),
    legend.position = "bottom",
    strip.background = element_blank(),
    strip.text = element_text(size = 25, face = "bold", color = "black"),
    panel.border = element_blank(),
    panel.background = element_rect(fill = "grey99", color = NA),
  )


################################################################################
#                          Base <-> Arbitrum (Latency)                         #
################################################################################

base_arb_data <- all_data[all_data$src_blockchain %in% c("base", "arbitrum") & all_data$dst_blockchain %in% c("base", "arbitrum"), ]

##### CCTP #####
cctp_df <- base_arb_data %>% filter(bridge == "cctp")

filtered_df_cctp <- cctp_df %>%
  filter(latency < 2000)

filtered_df_cctp <- filtered_df_cctp %>%
  group_by(bridge) %>%
  group_modify(~ sample_frac(.x, 0.1))

filtered_df_cctp_2 <- cctp_df %>%
  filter(latency >= 2000 & latency < 10000)

filtered_df_cctp_2 <- filtered_df_cctp_2 %>%
  group_by(bridge) %>%
  group_modify(~ sample_frac(.x, 0.75))

df_cctp_out_of_scope <- cctp_df %>%
  filter(!(latency < 10000))

cctp_sample <- rbind(filtered_df_cctp, filtered_df_cctp_2, df_cctp_out_of_scope)

##### CCIP #####
ccip_sample <- base_arb_data %>% filter(bridge == "ccip")

##### Stargate (Taxi) #####
stargate_taxi_df <- base_arb_data %>% filter(bridge == "stargate_oft")

filtered_df_stargate_taxi <- stargate_taxi_df %>%
  filter(latency < 50)

filtered_df_stargate_taxi <- filtered_df_stargate_taxi %>%
  group_by(bridge) %>%
  group_modify(~ sample_frac(.x, 0.05))

filtered_df_stargate_taxi_2 <- stargate_taxi_df %>%
  filter(latency >= 50 & latency < 70)

filtered_df_stargate_taxi_2 <- filtered_df_stargate_taxi_2 %>%
  group_by(bridge) %>%
  group_modify(~ sample_frac(.x, 0.1))

filtered_df_stargate_taxi_3 <- stargate_taxi_df %>%
  filter(latency > 70)

filtered_df_stargate_taxi_3 <- filtered_df_stargate_taxi_3 %>%
  group_by(bridge) %>%
  group_modify(~ sample_frac(.x, 0.5))

stargate_taxi_sample <- rbind(filtered_df_stargate_taxi, filtered_df_stargate_taxi_2, filtered_df_stargate_taxi_3)

##### Stargate (Bus) #####
stargate_bus_df <- base_arb_data %>% filter(bridge == "stargate_bus")

filtered_df_stargate_bus <- stargate_bus_df %>%
  filter(latency < 600)

filtered_df_stargate_bus <- filtered_df_stargate_bus %>%
  group_by(bridge) %>%
  group_modify(~ sample_frac(.x, 0.05))

df_stargate_bus_out_of_scope <- stargate_bus_df %>%
  filter(!(latency < 360))

stargate_bus_sample <- rbind(filtered_df_stargate_bus, df_stargate_bus_out_of_scope)

##### Across #####
across_df <- base_arb_data %>% filter(bridge == "across")

filtered_df_across <- across_df %>%
  filter(latency >= 0 & latency < 10)

filtered_df_across <- filtered_df_across %>%
  group_by(bridge) %>%
  group_modify(~ sample_frac(.x, 0.005))

filtered_df_across_2 <- across_df %>%
  filter(latency >= 10 & latency < 100)

filtered_df_across_2 <- filtered_df_across_2 %>%
  group_by(bridge) %>%
  group_modify(~ sample_frac(.x, 0.25))

filtered_df_across_3 <- across_df %>%
  filter(latency >= 100)

filtered_df_across_3 <- filtered_df_across_3 %>%
  group_by(bridge) %>%
  group_modify(~ sample_frac(.x, 0.25))

df_across_out_of_scope <- across_df %>%
  filter(!(latency >= 0))

across_sample <- rbind(filtered_df_across, filtered_df_across_2, filtered_df_across_3, df_across_out_of_scope)

##### Merge All #####
base_arb_data_sample <-rbind(cctp_sample, ccip_sample, stargate_taxi_sample, stargate_bus_sample, across_sample)

custom_labels <- c(
  "ccip" = "Cross-Chain Interoperability Protocol (CCIP) by Chainlink",
  "cctp" = "Cross-Chain Transfer Protocol (CCTP) by Circle",
  "stargate_oft" = "Stargate (Taxi)",
  "stargate_bus" = "Stargate (Bus)",
  "across" = "Across"
)

symlog_trans <- function(base = 10, thr = 1, scale = 1){
  trans <- function(x)
    ifelse(abs(x) < thr, x, sign(x) * 
             (thr + scale * suppressWarnings(log(sign(x) * x / thr, base))))
  
  inv <- function(x)
    ifelse(abs(x) < thr, x, sign(x) * 
             base^((sign(x) * x - thr) / scale) * thr)
  
  breaks <- function(x){
    sgn <- sign(x[which.max(abs(x))])
    if(all(abs(x) < thr))
      pretty_breaks()(x)
    else if(prod(x) >= 0){
      if(min(abs(x)) < thr)
        sgn * unique(c(pretty_breaks()(c(min(abs(x)), thr)),
                       log_breaks(base)(c(max(abs(x)), thr))))
      else
        sgn * log_breaks(base)(sgn * x)
    } else {
      if(min(abs(x)) < thr)
        unique(c(sgn * log_breaks()(c(max(abs(x)), thr)),
                 pretty_breaks()(c(sgn * thr, x[which.min(abs(x))]))))
      else
        unique(c(-log_breaks(base)(c(thr, -x[1])),
                 pretty_breaks()(c(-thr, thr)),
                 log_breaks(base)(c(thr, x[2]))))
    }
  }
  trans_new(paste("symlog", thr, base, scale, sep = "-"), trans, inv, breaks)
}

ggplot(base_arb_data, aes(
  x = latency,
  y = ifelse(bridge == "across", output_amount_usd,
             ifelse(bridge == "stargate_bus", amount_received_ld_usd, amount_usd)
  ),
  color = src_blockchain
)) +
  geom_point(size = 0.5, alpha = 0.2) +
  facet_wrap(
    ~bridge,
    scales = "fixed",
    ncol = 1,
    labeller = labeller(bridge = custom_labels)
  ) +
  scale_color_manual(
    values = c("base" = "black", "arbitrum" = "#d00000"),
    labels = c(TeX(r'(Base $\rightarrow$ Arbitrum)'), TeX(r'(Arbitrum $\rightarrow$ Base)')),
    name = "Transfer Direction"
  ) +
  scale_x_continuous(
    limits = c(-10^1, 10^6),
    trans = symlog_trans(base = 10, thr = 1),
    breaks = c(-10, -1, 0, 1, 10, 100, 1000, 10000, 100000, 1000000),
    labels = c(-10, -1, 0, 1, 10, 100, "1,000", "10,000", "100,000", "1,000,000")
  ) +
  scale_y_log10(
    limits = c(10^-4, 10^6),
    breaks = scales::trans_breaks(log10, function(x) 10^x, 5),
    labels = function(x) {
      ifelse(x < 1,
             scales::dollar_format(accuracy = 0.0001)(x),
             scales::dollar_format()(x)
      )
    }
  ) +
  labs(
    x = "CCTX Latency (seconds)",
    y = "Value Transferred (USD)",
    color = "Source Blockchain"
  ) +
  theme_linedraw(base_family = "Times New Roman") +
  theme(
    plot.title = element_text(
      face = "bold", size = 25, hjust = 0.5, vjust = -1
    ),
    plot.margin = unit(c(0, 0.2, 0, 0), "cm"),
    text = element_text(family = "serif"),
    axis.title.y = element_text(size = 25, face = "bold", vjust = 1),
    axis.title.x = element_text(size = 25, face = "bold", vjust = -2),
    axis.line = element_line(color = "black", linewidth = 0.3),
    axis.text = element_text(size = 25, face = "bold"),
    panel.grid.major.y = element_blank(),
    panel.grid.major.x = element_line(
      color = "grey80", linewidth = 0.3, linetype = 2
    ),
    panel.grid.minor.x = element_blank(),
    panel.grid.minor.y = element_blank(),
    legend.title = element_text(face = "bold", size = 25),
    legend.text = element_text(size = 25),
    legend.position = "bottom",
    strip.background = element_blank(),
    strip.text = element_text(size = 25, face = "bold", color = "black"),
    panel.border = element_blank(),
    panel.background = element_rect(fill = "grey99", color = NA),
    legend.margin = margin(0, 0, 0, 0)
  )

################################################################################
#                          Base <-> Arbitrum (Cost)                            #
################################################################################

base_arb_data_cost <- base_arb_data[base_arb_data$bridge %in% c("across", "stargate_bus"), ]

base_arb_data_sample <- base_arb_data_cost %>%
  group_by(bridge) %>%
  group_modify(~ sample_frac(.x, 0.2))

base_arb_data_sample <- base_arb_data_cost %>%
  group_by(bridge) %>%
  group_modify(~ {
    if (.y$bridge == "across") {
      .x <- .x %>%
        filter(!(user_cost > 0 & user_cost <= 0.5 & output_amount_usd >= 1 & output_amount_usd <= 1000)) %>%
        sample_frac(0.75)
    } else if (.y$bridge == "stargate_bus") {
      .x <- .x %>%
        filter(!(user_cost > 0 & user_cost <= 0.5 & amount_received_ld_usd >= 0.1 & amount_received_ld_usd <= 5000)) %>%
        sample_frac(0.75)
    }
    .x
  })

across_df <- base_arb_data_cost %>% filter(bridge == "across")

filtered_df_across <- across_df %>%
  filter(user_cost > 0 & user_cost <= 0.5 & output_amount_usd <= 10000)

filtered_df_across <- filtered_df_across %>%
  group_by(bridge) %>%
  group_modify(~ sample_frac(.x, 0.1))

filtered_df_across_2 <- across_df %>%
  filter(user_cost > 0.5 & user_cost <= 1 & output_amount_usd <= 10000)

filtered_df_across_2 <- filtered_df_across_2 %>%
  group_by(bridge) %>%
  group_modify(~ sample_frac(.x, 0.2))

filtered_df_across_4 <- across_df %>%
  filter(user_cost > 1)

filtered_df_across_4 <- filtered_df_across_4 %>%
  group_by(bridge) %>%
  group_modify(~ sample_frac(.x, 0.1))

filtered_df_across_out_of_scope <- across_df %>%
  filter(!(user_cost > 0 & output_amount_usd <= 10000))

merged_filtered_df_across <- rbind(filtered_df_across, filtered_df_across_2, filtered_df_across_4)


## Stargate bus

stargate_bus_df <- base_arb_data_cost %>% filter(bridge == "stargate_bus")

filtered_df_stargate_bus <- stargate_bus_df %>%
  filter(user_cost > 0 & user_cost <= 0.5 & amount_received_ld_usd <= 100000)

filtered_df_stargate_bus <- filtered_df_stargate_bus %>%
  group_by(bridge) %>%
  group_modify(~ sample_frac(.x, 0.1))


filtered_df_stargate_bus_2 <- stargate_bus_df %>%
  filter(user_cost > 0.5 & user_cost <= 1 & amount_received_ld_usd <= 100000)

filtered_df_stargate_bus_2 <- filtered_df_stargate_bus_2 %>%
  group_by(bridge) %>%
  group_modify(~ sample_frac(.x, 0.2))


filtered_df_stargate_bus_3 <- stargate_bus_df %>%
  filter(user_cost > 1)

filtered_df_stargate_bus_3 <- filtered_df_stargate_bus_3 %>%
  group_by(bridge) %>%
  group_modify(~ sample_frac(.x, 0.5))

filtered_df_stargate_bus_out_of_scope <- stargate_bus_df %>%
  filter(!(user_cost > 0 & amount_received_ld_usd <= 100000))


merged_filtered_df_stargate_bus <- rbind(filtered_df_stargate_bus, filtered_df_stargate_bus_2, filtered_df_stargate_bus_3, filtered_df_stargate_bus_out_of_scope)

#print_df = rbind(merged_filtered_df_stargate_bus, merged_filtered_df_across)
print_df = rbind(stargate_bus_df, across_df)

custom_labels <- c(
  "stargate_bus" = "Stargate (Bus)",
  "across" = "Across"
)

ggplot(print_df, aes(
  x = user_cost,
  y = ifelse(bridge == "across", output_amount_usd,
             ifelse(bridge == "stargate_bus", amount_received_ld_usd, amount_usd)
  ),
  color = src_symbol
)) +
  geom_point(size = 2, alpha = 0.8, shape = 21, color = "white", aes(fill = src_symbol)) +
  scale_fill_manual(
    values = c("WETH" = "#1f78b4", "USDC" = "red", "DAI" = "#00ff08", "USDT" = "#eeff00", "BAL" = "#000000", "POOL" = "#b15928"),
    name = "Symbol of Token Transacted"
  ) +
  facet_wrap(
    ~bridge,
    scales = "fixed",
    nrow = 1,
    labeller = labeller(bridge = custom_labels)
  ) +
  scale_x_continuous(
    limits = c(-10^0, 10^2),
    trans = symlog_trans(base = 10, thr = 1),
    breaks = c(-10, -1, 0, 1, 10, 100, 1000, 10000),
    labels = function(x) {
      ifelse(x < 1,
             scales::dollar_format()(x),
             scales::dollar_format()(x)
      )
    }
  ) +
  scale_y_log10(
    limits = c(0.01, 10^6),
    breaks = scales::trans_breaks(log10, function(x) 10^x, 10),
    labels = function(x) {
      ifelse(x < 1,
             scales::dollar_format(accuracy = 0.0001)(x),
             scales::dollar_format()(x)
      )
    }
  ) +
  labs(
    x = "User Cost (USD)",
    y = "Value Transferred (USD)",
    color = "Dst Token Symbol"
  ) +
  theme_linedraw(base_family = "Times New Roman") +
  theme(
    plot.title = element_text(
      face = "bold", size = 16, hjust = 0.5, vjust = -1
    ),
    plot.margin = unit(c(0, 0.2, 0, 0), "cm"),
    text = element_text(family = "serif"),
    axis.title.y = element_text(size = 24, face = "bold", vjust = 1),
    axis.title.x = element_text(size = 24, face = "bold", vjust = -2),
    axis.text = element_text(size = 20, face = "bold"),
    axis.line = element_line(color = "black", linewidth = 0.1),
    panel.grid.major.y = element_blank(),
    panel.grid.major.x = element_line(
      color = "grey10", linewidth = 0.1, linetype = 2,
    ),
    panel.grid.minor.x = element_blank(),
    panel.grid.minor.y = element_blank(),
    legend.title = element_text(face = "bold", size = 24),
    legend.text = element_text(size = 24),
    legend.position = "bottom",
    strip.background = element_blank(),
    strip.text = element_text(size = 24, face = "bold", color = "black"),
    panel.border = element_blank(),
    panel.background = element_rect(fill = "grey99", color = NA),
  )


################################################################################
#                    Stargate Bus Fees vs. Ethereum Gas Price                  #
################################################################################

stargate_bus_data = fread("../data/stargate_bus.csv", select = c("src_blockchain", "dst_blockchain", "user_timestamp", "amount_sent_ld_usd", "amount_received_ld_usd", "bus_fare"))

# create new col protocol_fee = amount_sent_ld_usd - amount_received_ld_usd
stargate_bus_data <- stargate_bus_data %>% 
  mutate(
    protocol_fee = amount_sent_ld_usd - amount_received_ld_usd
  )

# convert date but do not keep the time
stargate_bus_data$user_timestamp <- as.POSIXct(stargate_bus_data$user_timestamp, format = "%Y-%m-%d %H:%M:%S")
stargate_bus_data$user_timestamp <- as.Date(stargate_bus_data$user_timestamp)

# aggregate the same days and sum the values (protocol_fee) and bus_fare
stargate_bus_data <- stargate_bus_data %>% 
  group_by(user_timestamp) %>% 
  summarise(protocol_fee = sum(protocol_fee), bus_fare = sum(bus_fare))


# with header Date(UTC), UnixTimeStamp, Value (Wei) but with names: date, unix_ts, value_wei
gas_price_data <- fread("../data/gas_price_raw.csv", select = c("Date(UTC)", "Value (Wei)"))

# rename headers
setnames(gas_price_data, c("Date(UTC)", "Value (Wei)"), c("date", "value_wei"))

gas_price_data <- gas_price_data %>% 
  mutate(
    date = as.Date(date, format = "%m/%d/%Y")
  )

# Merge the datasets by date
merged_data <- merge(stargate_bus_data, gas_price_data, by.x = "user_timestamp", by.y = "date", all = TRUE)

# drop na in the protocol_fee column
merged_data <- merged_data[!is.na(merged_data$value_wei), ]

# we will need to normalize the values of the protocol_fee and value_wei between 0 and 1
merged_data$protocol_fee_norm <- (merged_data$protocol_fee - min(merged_data$protocol_fee)) / (max(merged_data$protocol_fee) - min(merged_data$protocol_fee))

merged_data$bus_fare <- as.numeric(merged_data$bus_fare)
merged_data$bus_fare_norm <- (merged_data$bus_fare - min(merged_data$bus_fare)) /
  (max(merged_data$bus_fare) - min(merged_data$bus_fare))

merged_data$value_wei <- as.numeric(merged_data$value_wei)
merged_data$value_wei_norm <- (merged_data$value_wei - min(merged_data$value_wei)) /
  (max(merged_data$value_wei) - min(merged_data$value_wei))

# plot them together based on the date to see if there is any correlation, make them with linewidths low and gas price dotted line
p1 <- ggplot(merged_data, aes(
  x = user_timestamp,
  y = bus_fare_norm,
  color = "Bus Fare"
)) +
  geom_line(size = 0.5) +
  geom_line(aes(y = value_wei_norm, color = "Gas Price"), linetype = "dotted", size = 0.5) +
  scale_color_manual(
    values = c("Bus Fare" = "red", "Gas Price" = "blue"),
    name = "Metric"
  ) +
  labs(
    x = "Date",
    y = "Normalized Value",
    color = "Metric"
  ) +
  scale_x_date(date_breaks = "1 month", date_labels = "%b %Y") +
  theme_linedraw(base_family = "Times New Roman") +
  theme(
    plot.title = element_text(
      face = "bold", size = 15, hjust = 0.5, vjust = -1
    ),
    plot.margin = unit(c(0, 0, 0.5, 0), "cm"),
    text = element_text(family = "serif"),
    axis.title.y = element_text(size = 14, face = "bold", vjust = 1),
    axis.title.x = element_text(size = 14, face = "bold", vjust = -1),
    axis.text = element_text(size = 12, vjust = 1),
    axis.line = element_line(color = "black", linewidth = 0.1),
    panel.grid.major.y = element_blank(),
    panel.grid.major.x = element_line(
      color = "grey80", linewidth = 0.1, linetype = 2
    ),
    panel.grid.minor.x = element_blank(),
    panel.grid.minor.y = element_blank(),
    panel.border = element_blank(),
    panel.background = element_rect(fill = "grey99", color = NA),
    legend.title = element_text(face = "bold", size=14, margin = margin(r = 5, b = 10)),
    legend.background = element_rect(fill="white"),
    legend.text = element_text(size = 12),
  )

p2 <- ggplot(merged_data, aes(
  x = user_timestamp,
  y = protocol_fee_norm,
  color = "Protocol Fee"
)) +
  geom_line(size = 0.5) +
  geom_line(aes(y = value_wei_norm, color = "Gas Price"), linetype = "dotted", size = 0.5) +
  scale_color_manual(
    values = c("Protocol Fee" = "red", "Gas Price" = "blue"),
    name = "Metric",
    breaks = c("Protocol Fee", "Gas Price")
  ) +
  labs(
    x = "Date",
    y = "Normalized Value",
    color = "Metric"
  ) +
  scale_x_date(date_breaks = "1 month", date_labels = "%b %Y") +
  theme_linedraw(base_family = "Times New Roman") +
  theme(
    plot.title = element_text(
      face = "bold", size = 15, hjust = 0.5, vjust = -1
    ),
    plot.margin = unit(c(0, 0, 0.5, 0), "cm"),
    text = element_text(family = "serif"),
    axis.title.y = element_text(size = 14, face = "bold", vjust = 1),
    axis.title.x = element_text(size = 14, face = "bold", vjust = -1),
    axis.text = element_text(size = 12, vjust = 1),
    axis.line = element_line(color = "black", linewidth = 0.1),
    panel.grid.major.y = element_blank(),
    panel.grid.major.x = element_line(
      color = "grey80", linewidth = 0.1, linetype = 2
    ),
    panel.grid.minor.x = element_blank(),
    panel.grid.minor.y = element_blank(),
    panel.border = element_blank(),
    panel.background = element_rect(fill = "grey99", color = NA),
    legend.title = element_text(face = "bold", size=14, margin = margin(r = 5, b = 10)),
    legend.background = element_rect(fill="white"),
    legend.text = element_text(size = 12),
  )

grid.arrange(p1, p2, nrow=1)



################################################################################
#                 Across Protocol Fees vs. Ethereum Gas Price                  #
################################################################################

across_data = fread("../data/across.csv", select = c("src_blockchain", "dst_blockchain", "user_timestamp", "input_amount_usd", "output_amount_usd"))

# create new col protocol_fee = amount_sent_ld_usd - amount_received_ld_usd
across_data <- across_data %>% 
  mutate(
    protocol_fee = input_amount_usd - output_amount_usd
  )

# convert date but do not keep the time
across_data$user_timestamp <- as.POSIXct(across_data$user_timestamp, format = "%Y-%m-%d %H:%M:%S")
across_data$user_timestamp <- as.Date(across_data$user_timestamp)

# aggregate the same days and sum the values (protocol_fee) and bus_fare
across_data <- across_data %>% 
  group_by(user_timestamp) %>% 
  summarise(protocol_fee = sum(protocol_fee))


# with header Date(UTC), UnixTimeStamp, Value (Wei) but with names: date, unix_ts, value_wei
gas_price_data <- fread("../data/gas_price_raw.csv", select = c("Date(UTC)", "Value (Wei)"))

# rename headers
setnames(gas_price_data, c("Date(UTC)", "Value (Wei)"), c("date", "value_wei"))

gas_price_data <- gas_price_data %>% 
  mutate(
    date = as.Date(date, format = "%m/%d/%Y")
  )

# Merge the datasets by date
merged_data <- merge(stargate_bus_data, gas_price_data, by.x = "user_timestamp", by.y = "date", all = TRUE)

# drop na in the protocol_fee column
merged_data <- merged_data[!is.na(merged_data$value_wei), ]

# we will need to normalize the values of the protocol_fee and value_wei between 0 and 1
merged_data$protocol_fee_norm <- (merged_data$protocol_fee - min(merged_data$protocol_fee)) / (max(merged_data$protocol_fee) - min(merged_data$protocol_fee))

merged_data$value_wei <- as.numeric(merged_data$value_wei)
merged_data$value_wei_norm <- (merged_data$value_wei - min(merged_data$value_wei)) /
  (max(merged_data$value_wei) - min(merged_data$value_wei))

ggplot(merged_data, aes(
  x = user_timestamp,
  y = protocol_fee_norm,
  color = "Protocol Fee"
)) +
  geom_line(size = 0.5) +
  geom_line(aes(y = value_wei_norm, color = "Gas Price"), linetype = "dotted", size = 0.5) +
  scale_color_manual(
    values = c("Protocol Fee" = "red", "Gas Price" = "blue"),
    name = "Metric",
    breaks = c("Protocol Fee", "Gas Price")
  ) +
  labs(
    x = "Date",
    y = "Normalized Value",
    color = "Metric"
  ) +
  scale_x_date(date_breaks = "1 month", date_labels = "%b %Y") +
  theme_linedraw(base_family = "Times New Roman") +
  theme(
    plot.title = element_text(
      face = "bold", size = 25, hjust = 0.5, vjust = -1
    ),
    plot.margin = unit(c(0, 0, 0.5, 0), "cm"),
    text = element_text(family = "serif"),
    axis.title.y = element_text(size = 25, face = "bold", vjust = 1),
    axis.title.x = element_text(size = 25, face = "bold", vjust = -1),
    axis.text = element_text(size = 25, vjust = 1),
    axis.line = element_line(color = "black", linewidth = 0.3),
    panel.grid.major.y = element_blank(),
    panel.grid.major.x = element_line(
      color = "grey80", linewidth = 0.1, linetype = 2
    ),
    panel.grid.minor.x = element_blank(),
    panel.grid.minor.y = element_blank(),
    panel.border = element_blank(),
    panel.background = element_rect(fill = "grey99", color = NA),
    legend.title = element_text(face = "bold", size=25, margin = margin(r = 5, b = 10)),
    legend.background = element_rect(fill="white"),
    legend.text = element_text(size = 25),
  )




################################################################################
#                  CCIP Protocol Fees vs. Ethereum Gas Price                   #
################################################################################

ccip_df <- fread("../data/ccip.csv", select = c("src_blockchain", "dst_blockchain", "src_timestamp", "fee_token", "fee_token_amount"))

# Convert src_timestamp to date
ccip_df$date <- as.POSIXct(ccip_df$src_timestamp, origin = "1970-01-01")

# only want datapoints where date is after 1st November 2024
ccip_df <- ccip_df %>%
  filter(date >= as.POSIXct("2024-11-01"))

# Filter the data
token_fee_base <- ccip_df %>%
  filter(src_blockchain == 'base' & fee_token == '0x4200000000000000000000000000000000000006' & dst_blockchain != "polygon")

token_fee_bnb <- ccip_df %>%
  filter(src_blockchain == 'bnb' & fee_token == '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c' & dst_blockchain != "polygon")


# Plot the data
p1 <- ggplot(token_fee_base, aes(x = date, y = fee_token_amount, color = dst_blockchain)) +
  geom_point(size = 1, alpha = 1) +
  scale_color_manual(
    values = c("arbitrum" = "#f67d7d", "avalanche" = "#7b7bff", "bnb" = "#55c855", "ethereum" = "#e2a83d", "linea" = "#c27bee", "optimism" = "#605f5f"),
    name = "Destination Blockchain",
    labels = c('Arbitrum', 'Avalanche', 'Binance Smart Chain', 'Ethereum', 'Linea', 'Optimism')
  ) +
  scale_y_log10() +
  labs(
    title = "a) WETH Transfers from Base",
    x = "Date",
    y = "Protocol Fee Value (Wei)",
  ) +
  theme_linedraw(base_family = "Times New Roman") +
  theme(
    plot.title = element_text(
      face = "bold", size = 20, hjust = 0.5, vjust = -1
    ),
    plot.margin = unit(c(0, 0.2, 0, 0), "cm"),
    text = element_text(family = "serif"),
    axis.title.y = element_text(size = 14, face = "bold", vjust = 1),
    axis.title.x = element_text(size = 14, face = "bold", vjust = 1),
    axis.text = element_text(size = 14, face = "bold"),
    axis.line = element_line(color = "black", linewidth = 0.2),
    panel.grid.major.y = element_blank(),
    panel.grid.major.x = element_line(
      color = "grey80", linewidth = 0.1, linetype = 2
    ),
    panel.grid.minor.x = element_blank(),
    panel.grid.minor.y = element_blank(),
    legend.title = element_text(face = "bold", size = 14),
    legend.text = element_text(size = 14),
    strip.background = element_blank(),
    strip.text = element_text(size = 14, face = "bold", color = "black"),
    panel.border = element_blank(),
    panel.background = element_rect(fill = "grey99", color = NA),
  )

p2 <- ggplot(token_fee_bnb, aes(x = date, y = fee_token_amount, color = dst_blockchain)) +
  geom_point(size = 1, alpha = 1) +
  scale_color_manual(
    values = c("arbitrum" = "#f67d7d", "avalanche" = "#7b7bff", "base" = "#55c855", "ethereum" = "#e2a83d", "linea" = "#c27bee", "optimism" = "#605f5f"),
    name = "Destination Blockchain",
    labels = c('Arbitrum', 'Avalanche', 'Base', 'Ethereum', 'Linea', 'Optimism')
  ) +
  scale_y_log10() +
  labs(
    title = "b) WBNB Transfers from BNB Chain",
    x = "Date",
    y = "Protocol Fee Value (Wei)",
  ) +
  theme_linedraw(base_family = "Times New Roman") +
  theme(
    plot.title = element_text(
      face = "bold", size = 20, hjust = 0.5, vjust = -1
    ),
    plot.margin = unit(c(0, 0.2, 0, 0), "cm"),
    text = element_text(family = "serif"),
    axis.title.y = element_text(size = 14, face = "bold", vjust = 1),
    axis.title.x = element_text(size = 14, face = "bold", vjust = 1),
    axis.text = element_text(size = 14, face = "bold"),
    axis.line = element_line(color = "black", linewidth = 0.2),
    panel.grid.major.y = element_blank(),
    panel.grid.major.x = element_line(
      color = "grey80", linewidth = 0.1, linetype = 2
    ),
    panel.grid.minor.x = element_blank(),
    panel.grid.minor.y = element_blank(),
    legend.title = element_text(face = "bold", size = 14),
    legend.text = element_text(size = 14),
    strip.background = element_blank(),
    strip.text = element_text(size = 14, face = "bold", color = "black"),
    panel.border = element_blank(),
    panel.background = element_rect(fill = "grey99", color = NA),
  )

grid.arrange(p1, p2, nrow=1)
