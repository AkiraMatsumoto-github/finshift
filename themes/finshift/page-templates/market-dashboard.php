<?php
/**
 * Template Name: Market Dashboard
 * Description: A dashboard-style page for specific regional markets (e.g., India, US).
 *
 * @package FinShift
 */

get_header();

// Get Custom Fields (Configuration)
$region_tag_slug = get_post_meta( get_the_ID(), 'market_region_tag', true ); // e.g., 'india-market'
$tv_symbol       = get_post_meta( get_the_ID(), 'market_tv_symbol', true ); // e.g., 'BSE:SENSEX'
$tv_symbol_desc  = get_post_meta( get_the_ID(), 'market_tv_desc', true );   // e.g., 'SENSEX'

// Metrics (Manual Input for Phase 1)
$metric_trend    = get_post_meta( get_the_ID(), '_metric_trend', true );
$metric_rsi      = get_post_meta( get_the_ID(), '_metric_rsi', true );
$metric_mom      = get_post_meta( get_the_ID(), '_metric_mom', true );
$metric_volatility = get_post_meta( get_the_ID(), '_metric_volatility', true );

// Fallbacks
if ( ! $region_tag_slug ) {
    $region_tag_slug = 'global'; // Fallback to global
}
?>

<main id="primary" class="site-main market-dashboard-page">
    
    <!-- Stick Header (Page Title) -->
    <header class="market-header">
        <div class="container">
            <div class="market-title-box">
                <h1 class="market-title"><?php the_title(); ?></h1>
            </div>
        </div>
    </header>

    <div class="container market-dashboard-grid">
        
        <!-- Main Content Column -->
        <div class="market-main-column">

            <!-- Market Pulse Section -->
            <section class="market-pulse-section">
                
                <!-- 1. Hero Chart (TradingView) -->
                <?php if ( $tv_symbol ) : ?>
                <div class="market-hero-chart">
                    <!-- TradingView Widget BEGIN -->
                    <div class="tradingview-widget-container">
                        <div id="tradingview_<?php echo esc_attr( md5( $tv_symbol ) ); ?>"></div>
                        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
                        <script type="text/javascript">
                        new TradingView.widget(
                        {
                            "width": "100%",
                            "height": 450,
                            "symbol": "<?php echo esc_js( $tv_symbol ); ?>",
                            "interval": "D",
                            "timezone": "Asia/Tokyo",
                            "theme": "light",
                            "style": "1",
                            "locale": "ja",
                            "toolbar_bg": "#f1f3f6",
                            "enable_publishing": false,
                            "hide_side_toolbar": false,
                            "allow_symbol_change": true,
                            "container_id": "tradingview_<?php echo esc_attr( md5( $tv_symbol ) ); ?>"
                        }
                        );
                        </script>
                    </div>
                </div>
                <?php endif; ?>

                <!-- 2. Key Metrics Panel -->
                <div class="market-metrics-panel">
                    <div class="metrics-scroller">
                        <div class="metric-card">
                            <span class="m-label">Trend (1M)</span>
                            <span class="m-value <?php echo ( floatval( $metric_trend ) >= 0 ) ? 'bull' : 'bear'; ?>">
                                <?php echo esc_html( $metric_trend ? $metric_trend : '-' ); ?>
                            </span>
                        </div>
                        <div class="metric-card">
                            <span class="m-label">RSI (14)</span>
                            <span class="m-value neutral">
                                <?php echo esc_html( $metric_rsi ? $metric_rsi : '-' ); ?>
                            </span>
                        </div>
                         <div class="metric-card">
                            <span class="m-label">Momentum (50D)</span>
                            <span class="m-value <?php echo ( floatval( $metric_mom ) >= 0 ) ? 'bull' : 'bear'; ?>">
                                 <?php echo esc_html( $metric_mom ? $metric_mom : '-' ); ?>
                            </span>
                        </div>
                        <div class="metric-card">
                            <span class="m-label">Volatility (20D)</span>
                            <span class="m-value neutral">
                                 <?php echo esc_html( $metric_volatility ? $metric_volatility : '-' ); ?>
                            </span>
                        </div>
                    </div>
                </div>

                <!-- 2.5 Today's Scenarios (From Latest Briefing) -->
                <?php
                // Tag Mapping for Query
                $tag_mapping = [
                    'us-market'    => 'us',
                    'india-market' => 'in',
                    'japan-market' => 'jp',
                    'china-market' => 'cn',
                    'indonesia-market' => 'ID',
                    'global'       => 'global'
                ];
                $query_tags = [ $region_tag_slug ];
                if ( isset( $tag_mapping[ $region_tag_slug ] ) ) {
                    $query_tags[] = $tag_mapping[ $region_tag_slug ];
                }

                $latest_briefing_args = array(
                    'category_name' => 'market-analysis',
                    'tag_slug__in'  => $query_tags,
                    'posts_per_page' => 1,
                    'orderby'       => 'date',
                    'order'         => 'DESC',
                );
                $latest_briefing_query = new WP_Query( $latest_briefing_args );
                
                if ( $latest_briefing_query->have_posts() ) :
                    $latest_briefing_query->the_post();
                    $bull_scen = get_post_meta( get_the_ID(), '_finshift_scenario_bull', true );
                    $bear_scen = get_post_meta( get_the_ID(), '_finshift_scenario_bear', true );
                    ?>
                    <div class="todays-scenarios-panel">
                        <h3 class="panel-title">Today's Market Scenarios</h3>
                        <div class="scenario-row">
                            <span class="scenario-label bull">楽観</span>
                            <span class="scenario-text"><?php echo $bull_scen ? esc_html( $bull_scen ) : '強気シナリオ: 最新記事で詳細を確認してください。'; ?></span>
                        </div>
                        <div class="scenario-row">
                            <span class="scenario-label bear">悲観</span>
                            <span class="scenario-text"><?php echo $bear_scen ? esc_html( $bear_scen ) : '弱気シナリオ: リスク要因と警戒ラインを確認してください。'; ?></span>
                        </div>
                        <div class="scenario-link">
                            <a href="<?php the_permalink(); ?>">Read Analysis from <?php echo get_the_date(); ?> ></a>
                        </div>
                    </div>
                    <?php
                    wp_reset_postdata();
                endif;
                ?>
            </section>

            <!-- 3. Daily Briefing Corner -->
            <section class="daily-briefing-wrapper">
                <div class="section-header-styled">
                    <h2 class="section-title">Daily Market Briefing</h2>
                </div>

                <?php
                // Re-use tags for list query
                $briefing_args = array(
                    'category_name' => 'market-analysis',
                    'tag_slug__in'  => $query_tags, 
                    'posts_per_page' => 5,
                    'orderby'       => 'date',
                    'order'         => 'DESC',
                );
                $briefing_query = new WP_Query( $briefing_args );

                if ( $briefing_query->have_posts() ) :
                    while ( $briefing_query->have_posts() ) :
                        $briefing_query->the_post();
                        // Get Region Label
                        $post_tags = get_the_tags();
                        $region_label = ($post_tags) ? $post_tags[0]->name : 'Global';

                        // Get Summary
                        $summary_json = get_post_meta(get_the_ID(), '_ai_structured_summary', true);
                        $summary_text = '';
                        if ($summary_json) {
                            $data = json_decode($summary_json, true);
                            if (json_last_error() === JSON_ERROR_NONE && !empty($data['summary'])) {
                                $summary_text = $data['summary'];
                            }
                        }
                        ?>
                        <article class="article-card dashboard-card">
                            <a href="<?php the_permalink(); ?>" class="card-overlay-link" aria-hidden="true" tabindex="-1"></a>
                            
                            <div class="dashboard-metrics">
                                <!-- Region -->
                                <div class="metric-box region-box">
                                    <span class="metric-label">MKT</span>
                                    <span class="region-badge-large"><?php echo esc_html($region_label); ?></span>
                                </div>
                                <!-- Regime -->
                                <div class="metric-box">
                                    <span class="metric-label">Regime</span>
                                    <span class="metric-value regime-<?php echo strtolower($regime); ?>"><?php echo $regime ? esc_html($regime) : '-'; ?></span>
                                </div>
                                <!-- Sentiment -->
                                <div class="metric-box">
                                    <span class="metric-label">Sentiment</span>
                                    <span class="metric-value sentiment-<?php echo $s_class; ?>"><?php echo $sentiment !== '' ? esc_html($sentiment) : '-'; ?></span>
                                </div>
                            </div>
                            
                            <h3 class="dashboard-title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3>
                            
                            <?php if ($summary_text) : ?>
                                <div class="dashboard-scenario-teaser">
                                    <span class="scenario-text"><?php echo esc_html($summary_text); ?></span>
                                </div>
                            <?php endif; ?>

                            <div class="dashboard-footer">
                                <span class="date-badge"><?php echo get_the_date('m/d'); ?></span>
                                <span class="read-briefing-text">Read Briefing &rarr;</span>
                            </div>
                        </article>
                        <?php
                    endwhile;
                    wp_reset_postdata();
                else :
                    echo '<p>No briefing available for this market yet.</p>';
                endif;
                ?>
            </section>

            <!-- 4. Featured News Corner -->
            <section class="featured-news-corner">
                <div class="section-header-styled">
                    <h2 class="section-title">Featured News</h2>
                </div>

                <div class="article-list-simple">
                    <?php
                    // Fetch Featured News
                    $news_args = array(
                        'category_name' => 'featured-news',
                        'tag'           => $region_tag_slug,
                        'posts_per_page' => 5,
                        'orderby'       => 'date',
                        'order'         => 'DESC',
                    );
                    $news_query = new WP_Query( $news_args );

                    if ( $news_query->have_posts() ) :
                        while ( $news_query->have_posts() ) :
                            $news_query->the_post();
                            ?>
                            <a href="<?php the_permalink(); ?>" class="market-article-item">
                                <?php if ( has_post_thumbnail() ) : ?>
                                    <?php the_post_thumbnail( 'thumbnail', array( 'class' => 'market-article-thumb' ) ); ?>
                                <?php else : ?>
                                    <div class="market-article-thumb" style="background:var(--color-bg-tertiary);"></div>
                                <?php endif; ?>
                                <div class="market-article-content">
                                    <h4 class="market-article-title"><?php the_title(); ?></h4>
                                    <span class="market-article-date"><?php echo get_the_date(); ?></span>
                                </div>
                            </a>
                            <?php
                        endwhile;
                        wp_reset_postdata();
                    else :
                        echo '<p>No featured news available.</p>';
                    endif;
                    ?>
                </div>
            </section>

        </div><!-- .market-main-column -->

        <!-- Sidebar Column -->
        <aside class="market-sidebar">
			<!-- Global Ranking Widget -->
            <div class="sidebar-widget-box">
                <h2 class="widget-title">Market Ranking</h2>
                 <?php
				if ( function_exists( 'finshift_get_popular_posts' ) ) {
					$popular_posts = finshift_get_popular_posts( 7, 5 );

					if ( ! empty( $popular_posts ) ) {
						$rank = 1;
						foreach ( $popular_posts as $post ) : 
							setup_postdata( $post );
							?>
                            <a href="<?php echo get_permalink( $post->ID ); ?>" class="ranking-item">
                                <span class="rank-number rank-<?php echo $rank; ?>"><?php echo $rank; ?></span>
                                <span class="rank-title"><?php echo get_the_title( $post->ID ); ?></span>
                            </a>
                            <?php
                            $rank++;
                        endforeach;
                        wp_reset_postdata();
                    }
                }
                ?>
            </div>
            
        </aside>

    </div><!-- .market-dashboard-grid -->
</main>

<?php
get_footer();
