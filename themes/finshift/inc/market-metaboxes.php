<?php
/**
 * Custom Metaboxes for FinShift Market Dashboard
 *
 * @package FinShift
 */

/**
 * Register Meta Box
 */
function finshift_add_market_meta_box() {
    $screens = [ 'page' ];
    foreach ( $screens as $screen ) {
        add_meta_box(
            'finshift_market_settings',           // Unique ID
            __( 'Market Dashboard Settings', 'finshift' ),  // Box title
            'finshift_market_meta_box_html',      // Content callback
            $screen,                              // Post type
            'side',                               // Context
            'high'                                // Priority
        );
    }
}
add_action( 'add_meta_boxes', 'finshift_add_market_meta_box' );

/**
 * Meta Box HTML
 */
function finshift_market_meta_box_html( $post ) {
    // Retrieve current values
    $region_tag = get_post_meta( $post->ID, 'market_region_tag', true );
    $tv_symbol  = get_post_meta( $post->ID, 'market_tv_symbol', true );
    
    // Metrics
    $metric_trend = get_post_meta( $post->ID, '_metric_trend', true );
    $metric_rsi   = get_post_meta( $post->ID, '_metric_rsi', true );
    $metric_mom   = get_post_meta( $post->ID, '_metric_mom', true ); // Using 'mom' for momentum

    ?>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
        
        <!-- Left Column: Configuration -->
        <div>
            <h4>Configuration</h4>
            <p>
                <label for="finshift_market_region_tag"><strong>Region Tag Slug</strong></label><br>
                <input type="text" name="market_region_tag" id="finshift_market_region_tag" value="<?php echo esc_attr( $region_tag ); ?>" class="widefat">
                <span class="description">e.g., <code>india-market</code>, <code>us-market</code></span>
            </p>
            <p>
                <label for="finshift_market_tv_symbol"><strong>TradingView Symbol</strong></label><br>
                <input type="text" name="market_tv_symbol" id="finshift_market_tv_symbol" value="<?php echo esc_attr( $tv_symbol ); ?>" class="widefat">
                <span class="description">e.g., <code>BSE:SENSEX</code>, <code>FRED:SP500</code></span>
            </p>
        </div>

        <!-- Right Column: Manual Metrics -->
        <div style="background: #f0f0f1; padding: 15px; border-radius: 4px;">
            <h4 style="margin-top:0;">Key Metrics (Manual Input)</h4>
            <p>
                <label for="finshift_metric_trend"><strong>Trend (1M %)</strong></label><br>
                <input type="text" name="_metric_trend" id="finshift_metric_trend" value="<?php echo esc_attr( $metric_trend ); ?>" style="width: 100%;">
                <span class="description">e.g., <code>+2.3%</code></span>
            </p>
            <p>
                <label for="finshift_metric_rsi"><strong>RSI (14)</strong></label><br>
                <input type="number" name="_metric_rsi" id="finshift_metric_rsi" value="<?php echo esc_attr( $metric_rsi ); ?>" style="width: 100%;">
                <span class="description">e.g., <code>65</code></span>
            </p>
            <p>
                <label for="finshift_metric_mom"><strong>Momentum (1M %)</strong></label><br>
                <input type="text" name="_metric_mom" id="finshift_metric_mom" value="<?php echo esc_attr( $metric_mom ); ?>" style="width: 100%;">
                <span class="description">e.g., <code>+5.4%</code></span>
            </p>
        </div>
    </div>
    <?php
}

/**
 * Save Meta Box Data
 */
function finshift_save_market_meta_box( $post_id ) {
    // Check auto save
    if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
        return;
    }
    // Check permissions
    if ( ! current_user_can( 'edit_page', $post_id ) ) {
        return;
    }

    // Save Fields
    $fields = [
        'market_region_tag',
        'market_tv_symbol',
        '_metric_trend',
        '_metric_rsi',
        '_metric_mom'
    ];

    foreach ( $fields as $field ) {
        if ( isset( $_POST[ $field ] ) ) {
            update_post_meta( $post_id, $field, sanitize_text_field( $_POST[ $field ] ) );
        }
    }
}
add_action( 'save_post', 'finshift_save_market_meta_box' );

/**
 * Register Meta for REST API
 * Required for automation scripts to update these fields via API.
 */
function finshift_register_market_rest_field() {
    $meta_keys = [
        'market_region_tag',
        'market_tv_symbol',
        '_metric_trend',
        '_metric_rsi',
        '_metric_mom',
        '_metric_ytd', // New: Year-to-Date metric
        '_metric_volatility' // New: Volatility metric
    ];

    foreach ( $meta_keys as $key ) {
        register_post_meta( 'page', $key, array(
            'show_in_rest' => true,
            'single'       => true,
            'type'         => 'string', // Use string for flexibility (e.g. "+2.3%")
            'auth_callback' => function() { return current_user_can( 'edit_posts' ); }
        ) );
    }
}
add_action( 'init', 'finshift_register_market_rest_field' );
